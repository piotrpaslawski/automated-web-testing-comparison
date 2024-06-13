import os
import sys
import inspect
from test_settings import *
from datetime import datetime as dt
from splinter import Browser


class SplinterTestingApp:
    def __init__(self, headless_mode):
        """
        This method sets up the Splinter testing application by creating
        the necessary directory for storing screenshots, initializing
        a Chrome WebDriver, and navigating to the specified testing 
        application URL. It also sets the window size for the WebDriver.

        Args:
            :headless_mode: (str) - Specifies whether the script should run in headless mode.
        """
        if not os.path.exists(SCREENSHOTS_SPLINTER_DIRECTORY):
            os.makedirs(SCREENSHOTS_SPLINTER_DIRECTORY)
        self.screenshot_id = 1

        if not os.path.exists(LOGS_SPLINTER_DIRECTORY):
            os.makedirs(LOGS_SPLINTER_DIRECTORY)
        current_datetime = dt.now().strftime('%Y%m%d-%H%M%S')
        log_filename = f"{LOGS_SPLINTER_DIRECTORY}/splinter_test_data_{current_datetime}.txt"
        self.log_file = open(log_filename, "w", encoding="utf-8")

        if headless_mode == "True":
            headless_mode = True
        else:
            headless_mode = False

        self.browser = Browser("chrome", headless=headless_mode)
        self.browser.visit(TESTING_APP_URL)
        self.browser.driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)

    def log(self, message):
        """
        Prints given message to console and log file.

        Args:
            :message: (str) - A message to display.
        """
        timestamp = dt.now().strftime("[%Y-%m-%d %H:%M:%S]")
        log_message = f"{timestamp} {message}"
        print(log_message)
        self.log_file.write(f"{log_message}\n")

    def run_all_test_cases(self):
        """
        Executes all test case methods whose names start with 'test_case_'.
        """
        test_cases = [
            method_name
            for method_name, _ in inspect.getmembers(self, predicate=inspect.ismethod)
            if method_name.startswith('test_case_')
        ]

        for test_case in test_cases:
            method = getattr(self, test_case)
            try:
                method()
            except AssertionError as e:
                self.log(f"{test_case.replace('_', ' ').replace('test', 'Test')}: FAILED! {str(e)}")

        self.log_file.close()

    def take_screenshot(self):
        """
        The method is used to capture a screenshot and save it to a file.
        """
        method_stacks = inspect.stack()
        test_name = method_stacks[1].function
        datetime = dt.now().strftime("%Y%m%d-%H%M%S")
        file_path = f"{SCREENSHOTS_SPLINTER_DIRECTORY}/{self.screenshot_id:02d}_{test_name}_{datetime}.png"
        self.browser.driver.save_screenshot(file_path)
        self.screenshot_id += 1

    def value_of_css_property(self, style, property):
        """
        Extracts the value of a specified CSS property from a given style string.

        Args:
            :style: (str) - A string containing CSS styles.
            :property: (str) - The CSS property whose value needs to be extracted.
        """
        return style.split(property)[1].split(';')[0].strip()

    def test_case_01(self):
        """
        Assert the title of the testing web application.
        """
        actual_title = self.browser.title
        assert PAGE_TITLE == actual_title, \
            f"Expected title: {PAGE_TITLE}, Actual title: {actual_title}."

        self.log("Test case 01: PASSED")

    def test_case_02(self):
        """
        Assert the presence of the main table on the page.
        """
        main_table = self.browser.find_by_id(TABLE_ID)
        assert main_table.visible, \
            "Main table is not displayed."

        self.log("Test case 02: PASSED")

    def test_case_03(self):
        """
        Assert the content of the header.
        """
        header = self.browser.find_by_tag(HEADER_TAG)
        actual_header_text = header.text
        assert HEADER_TEXT == actual_header_text, \
            f"Expected header: {HEADER_TEXT}, Actual header: {actual_header_text}."

        self.log("Test case 03: PASSED")

    def test_case_04(self):
        """
        Assert the dropdown functionality: display and hide.
        """
        dropdown_button = self.browser.find_by_id(HOVER_DROPDOWN_LIST_ID)
        dropdown_content = self.browser.find_by_css(f".{HOVER_DROPDOWN_LIST_CONTENT_CLASS}")

        dropdown_button.mouse_over()
        self.take_screenshot()
        assert dropdown_content.visible, \
            "Dropdown content is not displayed after hovering."

        main_table = self.browser.find_by_id(TABLE_ID)
        main_table.mouse_over()
        self.take_screenshot()
        assert not dropdown_content.visible, \
            "Dropdown content is still displayed after moving away."

        self.log("Test case 04: PASSED")

    def test_case_05(self):
        """
        Assert that selecting options from the dropdown list changes the default text.
        """
        dropdown_button = self.browser.find_by_id(HOVER_DROPDOWN_LIST_ID)
        dropdown_option_1 = self.browser.find_by_id(HOVER_DROPROWN_OPTION_1_ID)
        dropdown_option_2 = self.browser.find_by_id(HOVER_DROPROWN_OPTION_2_ID)
        dropdown_option_3 = self.browser.find_by_id(HOVER_DROPROWN_OPTION_3_ID)

        default_text_element = self.browser.find_by_tag(TEXT_AT_TOP_TAG)
        initial_default_text = default_text_element.text

        dropdown_button.mouse_over()
        dropdown_option_1.click()
        actual_text = default_text_element.text
        self.take_screenshot()
        assert actual_text == TEXT_1, \
            f"Default text not changed after selecting option 1, Actual text: {actual_text}."

        dropdown_button.mouse_over()
        dropdown_option_2.click()
        actual_text = default_text_element.text
        self.take_screenshot()
        assert actual_text == TEXT_2, \
            f"Default text not changed after selecting option 2, Actual text: {actual_text}."

        dropdown_button.mouse_over()
        dropdown_option_3.click()
        actual_text = default_text_element.text
        self.take_screenshot()
        assert actual_text == TEXT_3, \
            f"Default text not changed after selecting option 3, Actual text: {actual_text}."

        dropdown_button.click()
        self.take_screenshot()
        assert default_text_element.text == initial_default_text, \
            "Default text not reset after closing dropdown."

        self.log("Test case 05: PASSED")

    def test_case_06(self):
        """
        Assert that entering text in text fields sets the correct values.
        """
        single_line_textbox = self.browser.find_by_id(SINGLE_LINE_TEXTBOX_ID)
        expected_single_line_text = AUTHOR_NAME
        single_line_textbox.type(expected_single_line_text)
        actual_single_line_text = single_line_textbox.value
        self.take_screenshot()
        assert actual_single_line_text == expected_single_line_text, \
            f"Incorrect value in single-line textbox, Actual text: {actual_single_line_text}."

        multi_line_textbox = self.browser.find_by_id(MULTI_LINE_TEXTBOX_ID)
        expected_multi_line_text = f"{AUTHOR_NAME}\n{AUTHOR_NAME}"
        multi_line_textbox.type(expected_multi_line_text)
        actual_multi_line_text = multi_line_textbox.value
        self.take_screenshot()
        assert actual_multi_line_text == expected_multi_line_text, \
            f"Incorrect value in multi-line textbox, Actual text: {actual_multi_line_text}."

        self.log("Test case 06: PASSED")

    def test_case_07(self):
        """
        Assert the text in the placeholder of the textbox.
        """
        placeholder_textbox = self.browser.find_by_id(PLACEHOLDER_TEXTBOX_ID)
        actual_placeholder_text = placeholder_textbox[PLACEHOLDER]

        assert actual_placeholder_text == EXPECTED_PLACEHOLDER_TEXT, \
            (f"Placeholder text is not equal to expected text, "
             f"Expected: {EXPECTED_PLACEHOLDER_TEXT}, Actual: {actual_placeholder_text}.")

        self.log("Test case 07: PASSED")

    def test_case_08(self):
        """
        Assert that clicking the button changes text and colour in button, text field, and paragraph.
        """
        button_changing_colour = self.browser.find_by_id(BUTTON_CHANGING_COLOUR_ID)
        read_only_textbox = self.browser.find_by_id(READ_ONLY_TEXTBOX_ID)
        paragraph = self.browser.find_by_id(PARAGRAPH_ID)

        initial_button_colour = self.value_of_css_property(button_changing_colour[STYLE], COLOR)
        initial_read_only_textbox_text = read_only_textbox.value
        initial_read_only_textbox_colour = self.value_of_css_property(read_only_textbox[STYLE], COLOR)
        initial_paragraph_text = paragraph.text
        initial_paragraph_colour = paragraph[COLOR]

        button_changing_colour.click()
        self.take_screenshot()

        current_button_colour = self.value_of_css_property(button_changing_colour[STYLE], COLOR)
        assert current_button_colour != initial_button_colour, \
            "Button colour not changed after clicking."

        assert read_only_textbox.value != initial_read_only_textbox_text, \
            "Read only text value not changed after clicking."

        current_read_only_textbox_colour = self.value_of_css_property(read_only_textbox[STYLE], COLOR)
        assert current_read_only_textbox_colour != initial_read_only_textbox_colour, \
            "Read only colour value not changed after clicking."

        assert paragraph.text != initial_paragraph_text, \
            "Paragraph text not changed after clicking."

        afrer_change_paragraph_colour = self.value_of_css_property(paragraph[STYLE], COLOR)
        assert afrer_change_paragraph_colour != initial_paragraph_colour, \
            "Paragraph colour not changed after clicking."

        self.log("Test case 08: PASSED")

    def test_case_09(self):
        """
        Assert that the read-only text field is not editable.
        """
        read_only_text_field = self.browser.find_by_id(READ_ONLY_TEXTBOX_ID)
        try:
            read_only_text_field.clear()
            read_only_text_field.type(AUTHOR_NAME)
        except:
            pass
        assert read_only_text_field.value != AUTHOR_NAME, \
            "Read-only text field is editable."

        self.log("Test case 09: PASSED")

    def test_case_10(self):
        """
        Assert that the pre-filled textbox retains its value after editing other textboxes.
        """
        pre_filled_textbox = self.browser.find_by_id(PREFILLED_TEXTBOX_ID)
        other_textbox = self.browser.find_by_id(SINGLE_LINE_TEXTBOX_ID)

        initial_pre_filled_value = pre_filled_textbox.value
        other_textbox.clear()
        other_textbox.type(AUTHOR_NAME)
        self.take_screenshot()
        assert pre_filled_textbox.value == initial_pre_filled_value, \
            "Pre-filled textbox value changed after editing another textbox."

        self.log("Test case 10: PASSED")

    def test_case_11(self):
        """
        Assert that clicking the radio button selects it.
        """
        radio_button_1 = self.browser.find_by_id(RADIO_BUTTON_1_ID)
        radio_button_2 = self.browser.find_by_id(RADIO_BUTTON_2_ID)
        initial_state_radio_button_2 = radio_button_2.checked

        radio_button_1.click()
        assert not initial_state_radio_button_2, \
            "Radio button 2 is not deselected by default."
        assert radio_button_1.checked, \
            "Radio button 1 is not selected after clicking."
        assert not radio_button_2.checked, \
            "Radio button 2 is selected after clicking on radio button 1."

        radio_button_2.click()
        self.take_screenshot()
        assert not radio_button_1.checked, \
            "Radio button 1 is still selected after clicking on radio button 2."
        assert radio_button_2.checked, \
            "Radio button 2 is not selected after clicking."

        self.log("Test case 11: PASSED")

    def test_case_12(self):
        """
        Assert that the predefined checkbox is initially checked.
        """
        predefined_checkbox = self.browser.find_by_id(CHECKBOX_0_ID)
        assert predefined_checkbox.checked, \
            "Predefined checkbox is not checked by default."

        self.log("Test case 12: PASSED")

    def test_case_13(self):
        """
        Assert that clicking the checkbox sets it as checked.
        """
        example_checkbox = self.browser.find_by_id(CHECKBOX_2_ID)
        initial_state_checkbox = example_checkbox.checked

        example_checkbox.click()
        self.take_screenshot()
        assert not initial_state_checkbox, \
            "Example checkbox is not deselected by default."
        assert example_checkbox.checked, \
            "Example checkbox is not checked after clicking."

        self.log("Test case 13: PASSED")

    def test_case_14(self):
        """
        Assert that the checkbox is unchecked after clicking it twice.
        """
        example_checkbox = self.browser.find_by_id(CHECKBOX_1_ID)
        initial_state_checkbox = example_checkbox.checked

        example_checkbox.click()
        self.take_screenshot()
        assert example_checkbox.checked != initial_state_checkbox, \
            "Checkbox state not changed after the first click."

        example_checkbox.click()
        self.take_screenshot()
        assert example_checkbox.checked == initial_state_checkbox, \
            "Checkbox state not changed back after the second click."

        self.log("Test case 14: PASSED")

    def test_case_15(self):
        """
        Assert that clicking multiple checkboxes simultaneously checks them.
        """
        checkbox_1 = self.browser.find_by_id(CHECKBOX_1_ID)
        checkbox_2 = self.browser.find_by_id(CHECKBOX_2_ID)
        checkbox_3 = self.browser.find_by_id(CHECKBOX_3_ID)
        initial_state_checkbox_1 = checkbox_1.checked
        initial_state_checkbox_2 = checkbox_2.checked
        initial_state_checkbox_3 = checkbox_3.checked

        checkbox_1.click()
        checkbox_2.click()
        checkbox_3.click()
        self.take_screenshot()
        assert checkbox_1.checked != initial_state_checkbox_1, \
            "Checkbox 1 state not changed after simultaneous clicking."
        assert checkbox_2.checked != initial_state_checkbox_2, \
            "Checkbox 2 state not changed after simultaneous clicking."
        assert checkbox_3.checked != initial_state_checkbox_3, \
            "Checkbox 3 state not changed after simultaneous clicking."

        self.log("Test case 15: PASSED")

    def test_case_16(self):
        """
        Assert that moving the slider changes the progress bar.
        """
        slider = self.browser.find_by_id(SLIDER_ID)
        progress_bar = self.browser.find_by_id(PROGRESS_BAR_ID)

        initial_slider_value = slider[VALUE]
        initial_progress_bar_value = progress_bar[VALUE]
        assert initial_slider_value == initial_progress_bar_value, \
            (f"Slider value not equal to progress bar value, "
             f"Slider: {initial_slider_value}, Progress bar: {initial_progress_bar_value}.")

        self.browser.execute_script("arguments[0].value = arguments[1]", slider._element, int(initial_slider_value) + 10)
        self.browser.execute_script("arguments[0].oninput()", slider._element)
        self.take_screenshot()
        assert progress_bar[VALUE] != initial_progress_bar_value, \
            "Progress bar value not changed after moving the slider."

        self.log("Test case 16: PASSED")

    def test_case_17(self):
        """
        Assert that the progress bar value is updated when the slider is clicked.
        """
        slider = self.browser.find_by_id(SLIDER_ID)
        progress_bar = self.browser.find_by_id(PROGRESS_BAR_ID)
        initial_progress_bar_value = progress_bar[VALUE]

        slider.click()
        self.take_screenshot()
        progress_bar_value = progress_bar[VALUE]
        assert progress_bar_value != initial_progress_bar_value, \
            ("Progress bar value not changed after clicking the slider, "
             f"Current value: {progress_bar_value}, Initial value: {initial_progress_bar_value}.")

        self.log("Test case 17: PASSED")

    def test_case_18(self):
        """
        Assert that selecting an option in the select dropdown list changes the percentage indicator.
        """
        select_dropdown_list = self.browser.find_by_id(SELECT_DROPDOWN_LIST_ID)
        meter_bar = self.browser.find_by_id(PERCENTAGE_INDICATOR_BAR_ID)
        meter_label = self.browser.find_by_id(PERCENTAGE_INDICATOR_LABEL_ID)
        select_options = select_dropdown_list.find_by_tag(PERCENTAGE_INDICATOR_OPTION_TAG)

        initial_meter_bar_value = meter_bar[VALUE]
        initial_meter_label_text = meter_label.text

        select_options[1].click()
        self.take_screenshot()
        assert meter_bar[VALUE] != initial_meter_bar_value, \
            "Meter bar value not changed after selecting an option."
        assert meter_label.text != initial_meter_label_text, \
            "Meter label text not changed after selecting an option."

        self.log("Test case 18: PASSED")

    def test_case_19(self):
        """
        Assert that the percentage indicator value is not updated after clicking on the indicator.
        """
        meter_bar = self.browser.find_by_id(PERCENTAGE_INDICATOR_BAR_ID)
        meter_label = self.browser.find_by_id(PERCENTAGE_INDICATOR_LABEL_ID)

        initial_meter_bar_value = meter_bar[VALUE]
        initial_meter_label_text = meter_label.text

        meter_bar.click()
        self.take_screenshot()
        assert meter_bar[VALUE] == initial_meter_bar_value, \
            "Meter bar value not changed after clicking on the meter."
        assert meter_label.text == initial_meter_label_text, \
            "Meter label text not changed after clicking on the meter."

        self.log("Test case 19: PASSED")

    def test_case_20(self):
        """
        Assert that refreshing the page displays the testing web application.
        """
        self.browser.reload()

        self.browser.is_element_present_by_id(TABLE_ID, wait_time=10)
        main_table_after_refresh = self.browser.find_by_id(TABLE_ID)

        self.take_screenshot()
        assert main_table_after_refresh.visible, \
            "Main table is not displayed after refreshing the page."

        self.log("Test case 20: PASSED")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        headless_mode = sys.argv[1]
    else:
        headless_mode = "True"

    app = SplinterTestingApp(headless_mode)
    app.run_all_test_cases()
