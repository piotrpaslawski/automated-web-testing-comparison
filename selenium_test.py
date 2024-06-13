import os
import sys
import inspect
from test_settings import *
from datetime import datetime as dt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


class SeleniumTestingApp:
    def __init__(self, headless_mode):
        """
        This method sets up the Selenium testing application by creating
        the necessary directory for storing screenshots, initializing
        a Chrome WebDriver, and navigating to the specified testing 
        application URL. It also sets the window size for the WebDriver.

        Args:
            :headless_mode: (str) - Specifies whether the script should run in headless mode.
        """
        if not os.path.exists(SCREENSHOTS_SELENIUM_DIRECTORY):
            os.makedirs(SCREENSHOTS_SELENIUM_DIRECTORY)
        self.screenshot_id = 1

        if not os.path.exists(LOGS_SELENIUM_DIRECTORY):
            os.makedirs(LOGS_SELENIUM_DIRECTORY)
        current_datetime = dt.now().strftime('%Y%m%d-%H%M%S')
        log_filename = f"{LOGS_SELENIUM_DIRECTORY}/selenium_test_data_{current_datetime}.txt"
        self.log_file = open(log_filename, "w", encoding="utf-8")

        chrome_options = Options()
        if headless_mode == "True":
            chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get(TESTING_APP_URL)
        self.driver.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)

    def log(self, message):
        """
        Prints given message to console and log file.

        Args:
            :message: (str) - A message to display.
        """
        timestamp = dt.now().strftime("[%Y-%m-%d %H:%M:%S]")
        log_message = f"{timestamp} {message}"
        print(log_message)

        if self.log_file:
            with open(self.log_file.name, "a", encoding="utf-8") as file:
                file.write(f"{log_message}\n")
                file.flush()

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
        file_path = f"{SCREENSHOTS_SELENIUM_DIRECTORY}/{self.screenshot_id:02d}_{test_name}_{datetime}.png"
        self.driver.save_screenshot(file_path)
        self.screenshot_id += 1

    def test_case_01(self):
        """
        Assert the title of the testing web application.
        """
        actual_title = self.driver.title
        assert PAGE_TITLE == actual_title, \
            f"Expected title: {PAGE_TITLE}, Actual title: {actual_title}."

        self.log("Test case 01: PASSED")

    def test_case_02(self):
        """
        Assert the presence of the main table on the page.
        """
        main_table = self.driver.find_element(By.ID, TABLE_ID)
        assert main_table.is_displayed(), \
            "Main table is not displayed."

        self.log("Test case 02: PASSED")

    def test_case_03(self):
        """
        Assert the content of the header.
        """
        header = self.driver.find_element(By.TAG_NAME, HEADER_TAG)
        actual_header_text = header.text
        assert HEADER_TEXT == actual_header_text, \
            f"Expected header: {HEADER_TEXT}, Actual header: {actual_header_text}."

        self.log("Test case 03: PASSED")

    def test_case_04(self):
        """
        Assert the dropdown functionality: display and hide.
        """
        dropdown_button = self.driver.find_element(By.ID, HOVER_DROPDOWN_LIST_ID)
        dropdown_content = self.driver.find_element(By.CLASS_NAME, HOVER_DROPDOWN_LIST_CONTENT_CLASS)

        webdriver.ActionChains(self.driver).move_to_element(dropdown_button).perform()
        self.take_screenshot()
        assert dropdown_content.is_displayed(), \
            "Dropdown content is not displayed after hovering."

        webdriver.ActionChains(self.driver).move_to_element_with_offset(dropdown_button, -30, -30).perform()
        self.take_screenshot()
        assert not dropdown_content.is_displayed(), \
            "Dropdown content is still displayed after moving away."

        self.log("Test case 04: PASSED")

    def test_case_05(self):
        """
        Assert that selecting options from the dropdown list changes the default text.
        """
        dropdown_button = self.driver.find_element(By.ID, HOVER_DROPDOWN_LIST_ID)
        dropdown_option_1 = self.driver.find_element(By.ID, HOVER_DROPROWN_OPTION_1_ID)
        dropdown_option_2 = self.driver.find_element(By.ID, HOVER_DROPROWN_OPTION_2_ID)
        dropdown_option_3 = self.driver.find_element(By.ID, HOVER_DROPROWN_OPTION_3_ID)

        default_text_element = self.driver.find_element(By.TAG_NAME, TEXT_AT_TOP_TAG)
        initial_default_text = default_text_element.text

        webdriver.ActionChains(self.driver).move_to_element(dropdown_button).perform()
        dropdown_option_1.click()
        actual_text = default_text_element.text
        self.take_screenshot()
        assert actual_text == TEXT_1, \
            f"Default text not changed after selecting option 1, Actual text: {actual_text}."

        webdriver.ActionChains(self.driver).move_to_element(dropdown_button).perform()
        dropdown_option_2.click()
        actual_text = default_text_element.text
        self.take_screenshot()
        assert actual_text == TEXT_2, \
            f"Default text not changed after selecting option 2, Actual text: {actual_text}."

        webdriver.ActionChains(self.driver).move_to_element(dropdown_button).perform()
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
        single_line_textbox = self.driver.find_element(By.ID, SINGLE_LINE_TEXTBOX_ID)
        expected_single_line_text = AUTHOR_NAME
        single_line_textbox.clear()
        single_line_textbox.send_keys(expected_single_line_text)
        actual_single_line_text = single_line_textbox.get_attribute(VALUE)
        self.take_screenshot()
        assert actual_single_line_text == expected_single_line_text, \
            f"Incorrect value in single-line textbox, Actual text: {actual_single_line_text}."

        multi_line_textbox = self.driver.find_element(By.ID, MULTI_LINE_TEXTBOX_ID)
        expected_multi_line_text = f"{AUTHOR_NAME}\n{AUTHOR_NAME}"
        multi_line_textbox.clear()
        multi_line_textbox.send_keys(expected_multi_line_text)
        actual_multi_line_text = multi_line_textbox.get_attribute(VALUE)
        self.take_screenshot()
        assert actual_multi_line_text == expected_multi_line_text, \
            f"Incorrect value in multi-line textbox, Actual text: {actual_multi_line_text}."

        self.log("Test case 06: PASSED")

    def test_case_07(self):
        """
        Assert the text in the placeholder of the textbox.
        """
        placeholder_textbox = self.driver.find_element(By.ID, PLACEHOLDER_TEXTBOX_ID)
        actual_placeholder_text = placeholder_textbox.get_attribute(PLACEHOLDER)

        assert actual_placeholder_text == EXPECTED_PLACEHOLDER_TEXT, \
            (f"Placeholder text is not equal to expected text, "
             f"Expected: {EXPECTED_PLACEHOLDER_TEXT}, Actual: {actual_placeholder_text}.")

        self.log("Test case 07: PASSED")

    def test_case_08(self):
        """
        Assert that clicking the button changes text and colour in button, text field, and paragraph.
        """
        button_changing_colour = self.driver.find_element(By.ID, BUTTON_CHANGING_COLOUR_ID)
        read_only_textbox = self.driver.find_element(By.ID, READ_ONLY_TEXTBOX_ID)
        paragraph = self.driver.find_element(By.ID, PARAGRAPH_ID)

        initial_button_colour = button_changing_colour.value_of_css_property(COLOR)
        initial_read_only_textbox_text = read_only_textbox.get_attribute(VALUE)
        initial_read_only_textbox_colour = read_only_textbox.value_of_css_property(COLOR)
        initial_paragraph_text = paragraph.text
        initial_paragraph_colour = paragraph.value_of_css_property(COLOR)

        button_changing_colour.click()
        self.take_screenshot()

        assert button_changing_colour.value_of_css_property(COLOR) != initial_button_colour, \
            "Button colour not changed after clicking."

        assert read_only_textbox.get_attribute(VALUE) != initial_read_only_textbox_text, \
            "Read only text value not changed after clicking."

        assert read_only_textbox.value_of_css_property(COLOR) != initial_read_only_textbox_colour, \
            "Read only colour value not changed after clicking."

        assert paragraph.text != initial_paragraph_text, \
            "Paragraph text not changed after clicking."

        assert paragraph.value_of_css_property(COLOR) != initial_paragraph_colour, \
            "Paragraph colour not changed after clicking."

        self.log("Test case 08: PASSED")

    def test_case_09(self):
        """
        Assert that the read-only text field is not editable.
        """
        read_only_text_field = self.driver.find_element(By.ID, READ_ONLY_TEXTBOX_ID)
        try:
            read_only_text_field.clear()
            read_only_text_field.send_keys(AUTHOR_NAME)
        except:
            pass
        assert read_only_text_field.get_attribute(VALUE) != AUTHOR_NAME, \
            "Read-only text field is editable."

        self.log("Test case 09: PASSED")

    def test_case_10(self):
        """
        Assert that the pre-filled textbox retains its value after editing other textboxes.
        """
        pre_filled_textbox = self.driver.find_element(By.ID, PREFILLED_TEXTBOX_ID)
        other_textbox = self.driver.find_element(By.ID, SINGLE_LINE_TEXTBOX_ID)

        initial_pre_filled_value = pre_filled_textbox.get_attribute(VALUE)
        other_textbox.clear()
        other_textbox.send_keys(AUTHOR_NAME)
        self.take_screenshot()
        assert pre_filled_textbox.get_attribute(VALUE) == initial_pre_filled_value, \
            "Pre-filled textbox value changed after editing another textbox."

        self.log("Test case 10: PASSED")

    def test_case_11(self):
        """
        Assert that clicking the radio button selects it.
        """
        radio_button_1 = self.driver.find_element(By.ID, RADIO_BUTTON_1_ID)
        radio_button_2 = self.driver.find_element(By.ID, RADIO_BUTTON_2_ID)
        initial_state_radio_button_2 = radio_button_2.is_selected()

        radio_button_1.click()
        assert not initial_state_radio_button_2, \
            "Radio button 2 is not deselected by default."
        assert radio_button_1.is_selected(), \
            "Radio button 1 is not selected after clicking."
        assert not radio_button_2.is_selected(), \
            "Radio button 2 is selected after clicking on radio button 1."

        radio_button_2.click()
        self.take_screenshot()
        assert not radio_button_1.is_selected(), \
            "Radio button 1 is still selected after clicking on radio button 2."
        assert radio_button_2.is_selected(), \
            "Radio button 2 is not selected after clicking."

        self.log("Test case 11: PASSED")

    def test_case_12(self):
        """
        Assert that the predefined checkbox is initially checked.
        """
        predefined_checkbox = self.driver.find_element(By.ID, CHECKBOX_0_ID)
        assert predefined_checkbox.is_selected(), \
            "Predefined checkbox is not checked by default."

        self.log("Test case 12: PASSED")

    def test_case_13(self):
        """
        Assert that clicking the checkbox sets it as checked.
        """
        example_checkbox = self.driver.find_element(By.ID, CHECKBOX_2_ID)
        initial_state_checkbox = example_checkbox.is_selected()

        example_checkbox.click()
        self.take_screenshot()
        assert not initial_state_checkbox, \
            "Example checkbox is not deselected by default."
        assert example_checkbox.is_selected(), \
            "Example checkbox is not checked after clicking."

        self.log("Test case 13: PASSED")

    def test_case_14(self):
        """
        Assert that the checkbox is unchecked after clicking it twice.
        """
        example_checkbox = self.driver.find_element(By.ID, CHECKBOX_1_ID)
        initial_state_checkbox = example_checkbox.is_selected()

        example_checkbox.click()
        self.take_screenshot()
        assert example_checkbox.is_selected() != initial_state_checkbox, \
            "Checkbox state not changed after the first click."

        example_checkbox.click()
        self.take_screenshot()
        assert example_checkbox.is_selected() == initial_state_checkbox, \
            "Checkbox state not changed back after the second click."

        self.log("Test case 14: PASSED")

    def test_case_15(self):
        """
        Assert that clicking multiple checkboxes simultaneously checks them.
        """
        checkbox_1 = self.driver.find_element(By.ID, CHECKBOX_1_ID)
        checkbox_2 = self.driver.find_element(By.ID, CHECKBOX_2_ID)
        checkbox_3 = self.driver.find_element(By.ID, CHECKBOX_3_ID)
        initial_state_checkbox_1 = checkbox_1.is_selected()
        initial_state_checkbox_2 = checkbox_2.is_selected()
        initial_state_checkbox_3 = checkbox_3.is_selected()

        webdriver.ActionChains(self.driver).click(checkbox_1).click(checkbox_2).click(checkbox_3).perform()
        self.take_screenshot()
        assert checkbox_1.is_selected() != initial_state_checkbox_1, \
            "Checkbox 1 state not changed after simultaneous clicking."
        assert checkbox_2.is_selected() != initial_state_checkbox_2, \
            "Checkbox 2 state not changed after simultaneous clicking."
        assert checkbox_3.is_selected() != initial_state_checkbox_3, \
            "Checkbox 3 state not changed after simultaneous clicking."

        self.log("Test case 15: PASSED")

    def test_case_16(self):
        """
        Assert that moving the slider changes the progress bar.
        """
        slider = self.driver.find_element(By.ID, SLIDER_ID)
        progress_bar = self.driver.find_element(By.ID, PROGRESS_BAR_ID)

        initial_slider_value = slider.get_attribute(VALUE)
        initial_progress_bar_value = progress_bar.get_attribute(VALUE)
        assert initial_slider_value == initial_progress_bar_value, \
            (f"Slider value not equal to progress bar value, "
             f"Slider: {initial_slider_value}, Progress bar: {initial_progress_bar_value}.")

        webdriver.ActionChains(self.driver).move_to_element(slider).click_and_hold().move_by_offset(50, 0).release().perform()
        self.take_screenshot()
        assert progress_bar.get_attribute(VALUE) != initial_progress_bar_value, \
            "Progress bar value not changed after moving the slider."

        self.log("Test case 16: PASSED")

    def test_case_17(self):
        """
        Assert that the progress bar value is updated when the slider is clicked.
        """
        slider = self.driver.find_element(By.ID, SLIDER_ID)
        progress_bar = self.driver.find_element(By.ID, PROGRESS_BAR_ID)
        initial_progress_bar_value = progress_bar.get_attribute(VALUE)

        webdriver.ActionChains(self.driver).click(slider).perform()
        self.take_screenshot()
        progress_bar_value = progress_bar.get_attribute(VALUE)
        assert progress_bar_value != initial_progress_bar_value, \
            ("Progress bar value not changed after clicking the slider, "
             f"Current value: {progress_bar_value}, Initial value: {initial_progress_bar_value}.")

        self.log("Test case 17: PASSED")

    def test_case_18(self):
        """
        Assert that selecting an option in the select dropdown list changes the percentage indicator.
        """
        select_dropdown_list = self.driver.find_element(By.ID, SELECT_DROPDOWN_LIST_ID)
        meter_bar = self.driver.find_element(By.ID, PERCENTAGE_INDICATOR_BAR_ID)
        meter_label = self.driver.find_element(By.ID, PERCENTAGE_INDICATOR_LABEL_ID)
        select_options = select_dropdown_list.find_elements(By.TAG_NAME, PERCENTAGE_INDICATOR_OPTION_TAG)

        initial_meter_bar_value = meter_bar.get_attribute(VALUE)
        initial_meter_label_text = meter_label.text

        select_options[1].click()
        self.take_screenshot()
        assert meter_bar.get_attribute(VALUE) != initial_meter_bar_value, \
            "Meter bar value not changed after selecting an option."
        assert meter_label.text != initial_meter_label_text, \
            "Meter label text not changed after selecting an option."

        self.log("Test case 18: PASSED")

    def test_case_19(self):
        """
        Assert that the percentage indicator value is not updated after clicking on the indicator.
        """
        meter_bar = self.driver.find_element(By.ID, PERCENTAGE_INDICATOR_BAR_ID)
        meter_label = self.driver.find_element(By.ID, PERCENTAGE_INDICATOR_LABEL_ID)

        initial_meter_bar_value = meter_bar.get_attribute(VALUE)
        initial_meter_label_text = meter_label.text

        meter_bar.click()
        self.take_screenshot()
        assert meter_bar.get_attribute(VALUE) == initial_meter_bar_value, \
            "Meter bar value not changed after clicking on the meter."
        assert meter_label.text == initial_meter_label_text, \
            "Meter label text not changed after clicking on the meter."

        self.log("Test case 19: PASSED")

    def test_case_20(self):
        """
        Assert that refreshing the page displays the testing web application.
        """
        self.driver.refresh()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, TABLE_ID))
        )
        main_table_after_refresh = self.driver.find_element(By.ID, TABLE_ID)

        self.take_screenshot()
        assert main_table_after_refresh.is_displayed(), \
            "Main table is not displayed after refreshing the page."

        self.log("Test case 20: PASSED")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        headless_mode = sys.argv[1]
    else:
        headless_mode = "True"

    app = SeleniumTestingApp(headless_mode)
    app.run_all_test_cases()
