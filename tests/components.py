import unittest
from pybootstrapui import components


class TestPyBootstrapUIComponents(unittest.TestCase):
    def test_audio(self):
        audio = components.Audio('/source/1.mp3', '/source/1.ogg', classes=['class-1'],
                                 unique_id='audio1')
        self.assertIn('<audio', audio.construct())
        self.assertIn('1.ogg', audio.construct())

    def test_div(self):
        div = components.Div(components.HTMLElement(), classes=['class-1'], unique_id='div1')
        self.assertIn('<div', div.construct())
        self.assertIn('class-1', div.construct())

    def test_button(self):
        def callback(context):
            pass

        button = components.Button(label='Click Me', on_click=callback, type='button', style='secondary',
                                   classes=['class-1'], id='button1')
        self.assertIn('<button', button.construct())
        self.assertIn('Click Me', button.construct())

    def test_button_group(self):
        button1 = components.Button(label='Button 1', on_click=lambda x: None)
        button2 = components.Button(label='Button 2', on_click=lambda x: None)
        button_group = components.ButtonGroup(button1, button2, id='button_group1')
        self.assertIn('<div', button_group.construct())
        self.assertIn('Button 1', button_group.construct())
        self.assertIn('Button 2', button_group.construct())

    def test_card(self):
        header = components.Header('Card Header')
        body_element = components.Text('Card body content')
        card = components.Card(body_element, header=header, id='card1')
        self.assertIn('<div class="card', card.construct())
        self.assertIn('Card Header', card.construct())
        self.assertIn('Card body content', card.construct())

    def test_option(self):
        option = components.Option(label='Option 1', value='1', selected=True)
        self.assertIn('Option 1', option.construct())
        self.assertIn('selected', option.construct())


    def test_custom_html(self):
        custom_html = components.CustomHTML('<p>Custom HTML</p>')
        self.assertIn('<p>Custom HTML</p>', custom_html.construct())

    def test_form(self):
        input_element = components.TextInput(label='Name', id='input1')
        form = components.Form(input_element, id='form1', action='http://example.com')
        self.assertIn('<form', form.construct())
        self.assertIn('Name', form.construct())

    def test_grid_system(self):
        div1 = components.Div(classes=['col'])
        div2 = components.Div(classes=['col'])
        grid = components.GridSystem(div1, div2, row=True)
        self.assertIn('class="col"', grid.construct())


    def test_file_image(self):
        file_image = components.FileImage(file_path='D:\\chee.png', alt='File Image', id='file_image1')
        self.assertIn('<img', file_image.construct())
        self.assertIn('File Image', file_image.construct())

    def test_raw_image(self):
        raw_image = components.RawImage(image_content=b'binarydata', alt='Raw Image', id='raw_image1')
        self.assertIn('<img', raw_image.construct())
        self.assertIn('Raw Image', raw_image.construct())


    def test_url_image(self):
        url_image = components.URLImage('http://example.com/image.png', alt='URL Image', id='url_image1')
        self.assertIn('<img', url_image.construct())
        self.assertIn('URL Image', url_image.construct())

    def test_text_input(self):
        text_input = components.TextInput(label='Enter text', id='text_input1')
        self.assertIn('<input', text_input.construct())
        self.assertIn('Enter text', text_input.construct())

    def test_int_input(self):
        int_input = components.IntInput(label='Enter number', id='int_input1')
        self.assertIn('<input', int_input.construct())
        self.assertIn('Enter number', int_input.construct())

    def test_email_input(self):
        email_input = components.EmailInput(label='Enter email', id='email_input1')
        self.assertIn('<input', email_input.construct())
        self.assertIn('Enter email', email_input.construct())

    def test_password_input(self):
        password_input = components.PasswordInput(label='Enter password', id='password_input1')
        self.assertIn('<input', password_input.construct())
        self.assertIn('Enter password', password_input.construct())

    def test_text_area(self):
        text_area = components.TextArea(label='Enter text', id='text_area1')
        self.assertIn('<textarea', text_area.construct())
        self.assertIn('Enter text', text_area.construct())

    def test_hr(self):
        hr = components.Hr()
        self.assertIn('<hr', hr.construct())

    def test_br(self):
        br = components.Br()
        self.assertIn('<br', br.construct())

    def test_spacer(self):
        spacer = components.Spacer(margin_top='20px')
        self.assertIn('margin-top: 20px', spacer.construct())

    def test_list(self):
        list_element = components.ListElement(components.Text('Item 1'))
        list_component = components.List(list_element, id='list1')
        self.assertIn('<ul', list_component.construct())
        self.assertIn('Item 1', list_component.construct())

    def test_markdown(self):
        markdown = components.Markdown('# Heading', id='markdown1')
        self.assertIn('<h1', markdown.construct())

    def test_modal(self):
        modal = components.Modal(title='Modal Title')
        self.assertIn('Modal Title', modal.construct())


    def test_progress_bar(self):
        progress_bar = components.ProgressBar(value=50, label='Progress', id='progress_bar1')
        self.assertIn('<div class="progress-bar', progress_bar.construct())
        self.assertIn('aria-valuenow="50"', progress_bar.construct())
        self.assertIn('Progress', progress_bar.construct())

    def test_notification(self):
        notification = components.Notification(message='This is a notification', style='info', id='notification1')
        self.assertIn('class="alert alert-info', notification.construct())
        self.assertIn('This is a notification', notification.construct())

    def test_file_upload(self):
        file_upload = components.FileUpload(label='Upload File', id='file_upload1')
        self.assertIn('<input type="file"', file_upload.construct())
        self.assertIn('Upload File', file_upload.construct())

    def test_text(self):
        text = components.Text('Sample text', unique_id='text1')
        self.assertIn('Sample text', text.construct())

    def test_header(self):
        header = components.Header('Header Text', header_size=1, unique_id='header1')
        self.assertIn('<h1', header.construct())
        self.assertIn('Header Text', header.construct())

    def test_bootstrap_icon(self):
        icon = components.BootstrapIcon(icon_name='alarm')
        self.assertIn('<i class="bi bi-alarm"', icon.construct())

    def test_bold(self):
        bold_text = components.bold('Bold Text')
        self.assertIn('Bold Text</b>', bold_text)

    def test_italic(self):
        italic_text = components.italic('Italic Text')
        self.assertIn('<i>Italic Text</i>', italic_text)

    def test_link(self):
        link = components.Link('Example', href='http://example.com', unique_id='link1')
        self.assertIn('<a href="http://example.com"', link.construct())
        self.assertIn('Example', link.construct())

    def test_code(self):
        code = components.Code(code='print("Hello, World!")', unique_id='code1')
        self.assertIn('<pre', code.construct())
        self.assertIn('print(&quot;Hello, World!&quot;)', code.construct())

    def test_tooltip(self):
        tooltip = components.Tooltip(target='button1', content='Tooltip text', unique_id='tooltip1')
        self.assertIn('new bootstrap.Tooltip', tooltip.construct())
        self.assertIn('title: "Tooltip text"', tooltip.construct())

    def test_video(self):
        video = components.Video('D:\\юмор снобов.mp4', controls=True, unique_id='video1')
        self.assertIn('<video', video.construct())
        self.assertIn('src="D:\\юмор снобов.mp4"', video.construct())
        self.assertIn('controls', video.construct())


