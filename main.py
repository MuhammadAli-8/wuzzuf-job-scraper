from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
import csv

# Columns
job_title = []
company_name = []
location = []
job_date = []
job_link = []
applicants = []
experience = []
career_level = []
education_level = []
job_salary = []
job_category = []
job_description = []
job_requirement = []
related_skills = []
page_num = 0

search = input('Enter Job Title, Location or Company: ')

# Mapping of user input to career level strings
career_level_map = {
    '0': '',
    '1': 'Student',
    '2': 'Entry%20Level',
    '3': 'Experienced',
    '4': 'Manager'
}

# Display the options in a user-friendly way
print('''Choose Career Level: 
    0 for "All"
    1 for "Student"
    2 for "Entry Level"
    3 for "Experienced"
    4 for "Manager"
''')

# Loop until the user provides a valid input
while True:
    target_career_level = input('Please enter the number corresponding to your desired career level: ')
    if target_career_level in career_level_map:
        target_career_level = career_level_map[target_career_level]
        break
    else:
        print("Invalid input. Please enter a number between 1 and 4.")

# Your search URL construction code continues here...


word_list = search.split()
search_query = 'q='+''.join(f'{i}%20' for i in word_list)
website_url = f"https://wuzzuf.net/search/jobs?a=spbg&{search_query}&filters%5Bcareer_level%5D%5B0%5D={target_career_level}" if target_career_level != '' else f"https://wuzzuf.net/search/jobs?a=spbg&{search_query}"

# Initialize the Chrome WebDriver
driver = webdriver.Chrome()

try:
    # Open the website
    driver.get(website_url + '&start=0')
    
    # Wait until the total jobs element is present
    total_jobs_element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.css-xkh9ud > strong"))
    )
    total_jobs = int(total_jobs_element.text.replace(',', ''))
    
    num_of_records = int(input(f'There are {total_jobs} Jobs Found, How many do you want to Scrape? '))
    
    while num_of_records > total_jobs:
        num_of_records = int(input(f'There is not enough Data, Please choose a value within the range: {total_jobs}. '))
    
    while len(job_title) < num_of_records:
        driver.get(website_url + f"&start={page_num}")
        
        # Wait until job elements are present
        jobs = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "/html/body/div/div/div[3]/div/div/div[2]/div/div/div[1]/h2/a"))
        )
        
        for job in jobs:
            if len(job_title) >= num_of_records:
                break

            try:
                job_url = job.get_attribute('href')
                driver.get(job_url)

                # Wait for job title to be visible
                WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, "div.css-bjn8wh > h1"))
                )
                
                job_title.append(driver.find_element(By.CSS_SELECTOR, 'div.css-bjn8wh > h1').text)
                location.append(driver.find_element(By.CSS_SELECTOR, '#app > div > main > article > section.css-dy1y6u > div > strong').text.split('-')[-1].strip())
                
                try:
                    company_name.append(driver.find_element(By.CSS_SELECTOR, '#app > div > main > article > section.css-dy1y6u > div > strong > div > a').text)
                except NoSuchElementException:
                    company_name.append('Name Is Hidden')
                
                try:
                    applicants.append(driver.find_element(By.CSS_SELECTOR, "#app > div > main > article > section.css-dy1y6u > div > div.css-104dl8g > div > strong").text)
                except NoSuchElementException:
                    applicants.append("0")
                
                job_date.append(driver.find_element(By.CSS_SELECTOR, '#app > div > main > article > section.css-dy1y6u > div > span').text)
                experience.append(driver.find_element(By.CSS_SELECTOR, "#app > div > main > article > section.css-3kx5e2 > div:nth-child(2) > span.css-47jx3m > span").text)
                career_level.append(driver.find_element(By.CSS_SELECTOR, "#app > div > main > article > section.css-3kx5e2 > div:nth-child(3) > span.css-47jx3m > span").text)
                education_level.append(driver.find_element(By.CSS_SELECTOR, "#app > div > main > article > section.css-3kx5e2 > div:nth-child(4) > span.css-47jx3m > span").text)
                job_salary.append(driver.find_element(By.CSS_SELECTOR, '#app > div > main > article > section.css-3kx5e2 > div:nth-last-child(3) > span.css-47jx3m').text)
                
                job_categories_elements = driver.find_elements(By.CSS_SELECTOR, '#app > div > main > article > section.css-3kx5e2 > div.css-13sf2ik > ul > li > a > span')
                job_categories = [element.text for element in job_categories_elements]
                job_category.append(', '.join(job_categories))
                
                job_skills_elements = driver.find_elements(By.CSS_SELECTOR, '#app > div > main > article > section.css-3kx5e2 > div.css-s2o0yh > a > span > span > span')
                job_skills = [element.text for element in job_skills_elements]
                related_skills.append(', '.join(job_skills))
                
                job_descriptions_elements = driver.find_elements(By.CSS_SELECTOR, '#app > div > main > article > section:nth-child(4) > div > ul > li')
                job_descriptions = [element.text for element in job_descriptions_elements]
                job_description.append(', '.join(job_descriptions))
                
                job_requirements_elements = driver.find_elements(By.CSS_SELECTOR, '#app > div > main > article > section:nth-child(5) > div > ul > li')
                job_requirements = [element.text for element in job_requirements_elements]
                job_requirement.append(', '.join(job_requirements))
                
                job_link.append(job_url)

                print(f'Job {len(job_title)}/{num_of_records} Extracted Successfully.')

            except StaleElementReferenceException:
                # If a stale element reference occurs, re-find the element
                print(f"Stale element encountered. Retrying job {len(job_title)+1} extraction...")
                driver.get(job_url)
                continue
            
            finally:
                # Navigate back to the job listings page and re-find the jobs list
                driver.back()
                jobs = WebDriverWait(driver, 10).until(
                    EC.presence_of_all_elements_located((By.XPATH, "/html/body/div/div/div[3]/div/div/div[2]/div/div/div[1]/h2/a"))
                )
        
        page_num += 1

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Ensure all lists have the same length
    assert len(job_title) == len(company_name) == len(location) == len(job_date) == len(job_link) == len(applicants) == len(experience) == len(career_level) == len(education_level) == len(job_salary) == len(job_category) == len(job_description) == len(job_requirement) == len(related_skills), "Lists must have the same length"

    # Combine all lists into rows
    rows = zip(
        job_title, 
        company_name, 
        location, 
        job_date, 
        job_salary, 
        job_requirement, 
        job_description, 
        applicants, 
        experience, 
        career_level, 
        education_level, 
        job_category, 
        related_skills,
        job_link
    )

    # Specify the filename
    filename = f'{search}.csv'

    # Write lists to the CSV file
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow([
            "Job Title", 
            "Company Name", 
            "Location", 
            "Job Date", 
            "Salary", 
            "Job Requirement", 
            "Job Description", 
            "Number of Applicants", 
            "Experience", 
            "Career Level", 
            "Education Level", 
            "Job Category", 
            "Related Skills",
            "Job Link"
        ])
        # Write the data rows
        writer.writerows(rows)
    
    print(f"Data successfully written to {filename}")

    driver.quit()
