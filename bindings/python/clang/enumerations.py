#===- enumerations.py - Python Enumerations ------------------*- python -*--===#
#
#                     The LLVM Compiler Infrastructure
#
# This file is distributed under the University of Illinois Open Source
# License. See LICENSE.TXT for details.
#
#===------------------------------------------------------------------------===#

"""
Clang Enumerations
==================

This module provides static definitions of enumerations that exist in libclang.

Enumerations are typically defined as a list of tuples. The exported values are
typically munged into other types or classes at module load time.

All enumerations are centrally defined in this file so they are all grouped
together and easier to audit. And, maybe even one day this file will be
automatically generated by scanning the libclang headers!
"""

# Maps to CXTokenKind. Note that libclang maintains a separate set of token
# enumerations from the C++ API.
TokenKinds = [
    ('PUNCTUATION', 0),
    ('KEYWORD', 1),
    ('IDENTIFIER', 2),
    ('LITERAL', 3),
    ('COMMENT', 4),
]

# Maps to CXCommentKind.
CommentKinds = [
    ('NULL', 0),
    ('TEXT', 1),
    ('INLINE_COMMAND', 2),
    ('HTML_START_TAG', 3),
    ('HTML_END_TAG', 4),
    ('PARAGRAPH', 5),
    ('BLOCK_COMMAND', 6),
    ('PARAM_COMMAND', 7),
    ('TPARAM_COMMAND', 8),
    ('VERBATIM_BLOCK_COMMAND', 9),
    ('VERBATIM_BLOCK_LINE', 10),
    ('VERBATIM_LINE', 11),
    ('FULL_COMMENT', 12),
]

# Maps to CXCommentInlineCommandRenderKind.
InlineCommandRenderKinds = [
    ('NORMAL', 0),
    ('BOLD', 1),
    ('MONOSPACED', 2),
    ('EMPHASIZED', 3),
]

# Maps to CXCommentParamPassDirection.
ParamCommandDirections = [
    ('IN', 0),
    ('OUT', 1),
    ('IN_OUT', 2),
]

__all__ = [
  'TokenKinds',
  'CommentKinds',
  'InlineCommandRenderKinds',
  'ParamCommandDirections',
]
