import pytest
from fhir_server.elements import primitives
from sqlalchemy import Column


class TestMarkdownField(object):
    def test_markdown_paragraph(self):
        result = primitives.MarkdownField().process_bind_param(
            'paragraph string for markdown', 'postgres')
        assert result == 'paragraph string for markdown'

    def test_markdown_emphasis(self):
        result = primitives.MarkdownField().process_bind_param(
            '**Bold** *italic* [Link](http://a.com)', 'postgres')
        assert result == '**Bold** *italic* [Link](http://a.com)'

    def test_process_result_value(self):
        result = primitives.MarkdownField().process_result_value(
            'paragraph string for markdown', 'postgres')
        assert result == 'paragraph string for markdown'

    @pytest.fixture
    def TestDataTypesModel(self, Base, session):
        class TestDataTypesModel(Base):
            __tablename__ = 'circle_test'
            id = Column(primitives.IdField, primary_key=True)
            markdown_field = Column(primitives.StringField)

        session.execute("""
            CREATE TABLE circle_test (
                id TEXT, markdown_field TEXT);""")

        return TestDataTypesModel

    def test_valid_markdown_document(self, session, TestDataTypesModel):
        mark = '''
        # Heading 1

        some paragraph text for markdown_field that should be
        saved as is.

        another paragraph after 1 blank line
        * List
        * List
        * List

        - List
        - List
        - List

        1. One
        2. Two
        3. Three

        Horizontal rule below

        ---

        ## Heading 2

        ~~Strikethrough~~

        ![Image](http://url/a.png)

        ### Inline code

        ```
        print '3 backticks or'
        print 'indent 4 spaces'
        ```

        ```javascript
        var s = "JavaScript syntax highlighting";
        alert(s);
        ```

        ```python
        s = "Python syntax highlighting"
        print s
        ```

        #### Tables

        | Tables        | Are           | Cool  |
        | ------------- |:-------------:| -----:|
        | col 3 is      | right-aligned | $1600 |
        | col 2 is      | centered      |   $12 |
        | zebra stripes | are neat      |    $1 |

        ##### H5

        ###### H6
        '''

        post_data = TestDataTypesModel(
            id="yiydidbh",
            markdown_field=mark
        )

        session.add(post_data)
        session.commit()

        result = session.query(TestDataTypesModel).first()
        assert result.markdown_field == mark
