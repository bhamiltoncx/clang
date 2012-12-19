import gc

from clang.cindex import Comment
from clang.cindex import CommentKind
from clang.cindex import InlineCommandRenderKind
from clang.cindex import ParamCommandDirection
from .util import get_cursor
from .util import get_cursors
from .util import get_tu

def test_brief():
  tu = get_tu('/** @brief Function 1. */ int function1();')

  comment = _get_comments(tu.cursor)[0]
  block_command = [c for c in comment if c.is_block_command()][0]
  assert block_command.get_block_command_name() == 'brief'

  brief_text = block_command.get_block_command_paragraph()[0].get_text()
  assert 'Function 1.' in brief_text

def test_multiline_brief():
  content = '''
/**
 * @brief Do the mambo.
 *        (Not to be confused with the samba.)
 */
extern void do_mambo();
'''
  tu = get_tu(content)
  comment = _get_comments(tu.cursor)[0]
  block_command = [c for c in comment if c.is_block_command()][0]
  assert block_command.get_block_command_name() == 'brief'

  brief_text_lines = \
      [line.get_text() for line in block_command.get_block_command_paragraph()]

  assert 'Do the mambo.' in brief_text_lines[0]
  assert '(Not to be confused with the samba.)' in brief_text_lines[1]

def test_param_directions():
  content = '''
/**
 * @param [in] width Width in pixels.
 * @param height Height in pixels.
 * @param [out] size Size in pixels^2.
 * @param [in,out] error Set to true if overflow occurs.
 *                       If already true when called, this no-ops.
 */
extern void get_size(int width, int height, int *size, bool *error);
'''
  tu = get_tu(content)
  comment = _get_comments(tu.cursor)[0]
  param_commands = [c for c in comment if c.is_param_command()]
  assert len(param_commands) == 4

  assert param_commands[0].get_param_command_name() == 'width'
  assert param_commands[0].is_param_command_direction_explicit()
  assert param_commands[0].get_param_command_direction() == \
      ParamCommandDirection.IN
  lines = _get_first_paragraph_lines(param_commands[0])
  assert 'Width in pixels.' in lines[0]

  assert param_commands[1].get_param_command_name() == 'height'
  assert not param_commands[1].is_param_command_direction_explicit()
  lines = _get_first_paragraph_lines(param_commands[1])
  assert 'Height in pixels.' in lines[0]

  assert param_commands[2].get_param_command_name() == 'size'
  assert param_commands[2].is_param_command_direction_explicit()
  assert param_commands[2].get_param_command_direction() == \
      ParamCommandDirection.OUT
  lines = _get_first_paragraph_lines(param_commands[2])
  assert 'Size in pixels^2.' in lines[0]

  assert param_commands[3].get_param_command_name() == 'error'
  assert param_commands[3].is_param_command_direction_explicit()
  assert param_commands[3].get_param_command_direction() == \
      ParamCommandDirection.IN_OUT
  lines = _get_first_paragraph_lines(param_commands[3])
  assert 'Set to true if overflow occurs.' in lines[0]
  assert 'If already true when called, this no-ops.' in lines[1]

def test_template_params():
  content = '''
/**
 * @tparam C A class.
 * @tparam TT Another class.
 * @tparam T A type.
 * @param aaa A value.
 */
template<typename C, template<typename T> class TT>
void test(TT<int> aaa);
'''
  tu = get_tu(content, lang='cpp')
  comment = _get_comments(tu.cursor)[0]
  tparam_commands = [c for c in comment if c.is_template_param_command()]
  assert len(tparam_commands) == 3

  assert tparam_commands[0].get_template_param_command_name() == 'C'
  assert tparam_commands[0].is_template_param_command_position_valid()
  assert tparam_commands[0].get_template_param_command_depth() == 1
  assert tparam_commands[0].get_template_param_command_index(0) == 0
  lines = _get_first_paragraph_lines(tparam_commands[0])
  assert 'A class.' in lines[0]

  assert tparam_commands[1].get_template_param_command_name() == 'TT'
  assert tparam_commands[1].is_template_param_command_position_valid()
  assert tparam_commands[1].get_template_param_command_depth() == 1
  assert tparam_commands[1].get_template_param_command_index(0) == 1
  lines = _get_first_paragraph_lines(tparam_commands[1])
  assert 'Another class.' in lines[0]

  assert tparam_commands[2].get_template_param_command_name() == 'T'
  assert tparam_commands[2].is_template_param_command_position_valid()
  assert tparam_commands[2].get_template_param_command_depth() == 2
  assert tparam_commands[2].get_template_param_command_index(0) == 1
  assert tparam_commands[2].get_template_param_command_index(1) == 0
  lines = _get_first_paragraph_lines(tparam_commands[2])
  assert 'A type.' in lines[0]

def test_xml():
  content = r'''
/// \brief Aaa.
///
/// Bbb.
///
/// \param x2 Ddd.
/// \param x1 Ccc.
/// \returns Eee.
void comment_to_html_conversion_22(int x1, int x2);
'''
  tu = get_tu(content)
  comment = _get_comments(tu.cursor)[0]

  expected_xml = r'''<Function file="t.c" line="9" column="6"><Name>comment_to_html_conversion_22</Name><USR>c:@F@comment_to_html_conversion_22</USR><Declaration>void comment_to_html_conversion_22(int x1, int x2)</Declaration><Abstract><Para> Aaa.</Para></Abstract><Parameters><Parameter><Name>x1</Name><Index>0</Index><Direction isExplicit="0">in</Direction><Discussion><Para> Ccc. </Para></Discussion></Parameter><Parameter><Name>x2</Name><Index>1</Index><Direction isExplicit="0">in</Direction><Discussion><Para> Ddd. </Para></Discussion></Parameter></Parameters><ResultDiscussion><Para> Eee.</Para></ResultDiscussion><Discussion><Para> Bbb.</Para></Discussion></Function>'''

  assert comment.get_full_comment_as_xml() == expected_xml

def test_html():
  content = r'''
/// \function foo
/// \class foo
/// \method foo
/// \interface foo
/// Blah blah.
void comment_to_html_conversion_25();
'''
  tu = get_tu(content)
  comment = _get_comments(tu.cursor)[0]

  expected_html = r'''<p class="para-brief"> Blah blah.</p>'''

  assert comment.get_full_comment_as_html() == expected_html

def _get_comments(cursor):
  comment_nodes = []
  for node in cursor.get_children():
    comment = node.get_parsed_comment()
    if not comment.is_null():
      comment_nodes.append(comment)
  return comment_nodes

def _get_first_paragraph_lines(node):
  first_paragraph = [c for c in node if c.kind == CommentKind.PARAGRAPH][0]
  return [c.get_text() for c in first_paragraph if c.is_text()]
