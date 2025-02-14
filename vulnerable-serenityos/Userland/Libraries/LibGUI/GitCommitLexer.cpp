/*
 * Copyright (c) 2022, Brian Gianforcaro <bgianf@serenityos.org>
 *
 * SPDX-License-Identifier: BSD-2-Clause
 */

#include <AK/CharacterTypes.h>
#include <AK/Vector.h>
#include <LibGUI/GitCommitLexer.h>

namespace GUI {

GitCommitLexer::GitCommitLexer(StringView input)
    : m_input(input)
{
}

char GitCommitLexer::peek(size_t offset) const
{
    if ((m_index + offset) >= m_input.length())
        return 0;
    return m_input[m_index + offset];
}

char GitCommitLexer::consume()
{
    VERIFY(m_index < m_input.length());
    char ch = m_input[m_index++];
    if (ch == '\n') {
        m_position.line++;
        m_position.column = 0;
    } else {
        m_position.column++;
    }
    return ch;
}

Vector<GitCommitToken> GitCommitLexer::lex()
{
    Vector<GitCommitToken> tokens;

    size_t token_start_index = 0;
    GitCommitPosition token_start_position;

    auto begin_token = [&] {
        token_start_index = m_index;
        token_start_position = m_position;
    };

    auto commit_token = [&](auto type) {
        GitCommitToken token;
        token.m_view = m_input.substring_view(token_start_index, m_index - token_start_index);
        token.m_type = type;
        token.m_start = token_start_position;
        token.m_end = m_position;
        tokens.append(token);
    };

    while (m_index < m_input.length()) {
        if (is_ascii_space(peek(0))) {
            begin_token();
            while (is_ascii_space(peek()))
                consume();
            continue;
        }

        // Commit comments
        if (peek(0) && peek(0) == '#') {
            begin_token();
            while (peek() && peek() != '\n')
                consume();
            commit_token(GitCommitToken::Type::Comment);
            continue;
        }

        consume();
        commit_token(GitCommitToken::Type::Unknown);
    }
    return tokens;
}

}
