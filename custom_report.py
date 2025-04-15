from bs4 import BeautifulSoup

with open('locust_report.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

css_link = soup.new_tag('link', rel='stylesheet', href='/tmp/styles/custom_style.css')
soup.head.append(css_link)

summary_section = soup.new_tag('div', attrs={'class': 'summary-section'})
header = soup.new_tag('h1')
header.string = 'Load Test Summary'
summary_section.append(header)

def extract_metric(label):
    row = soup.find('td', string=label)
    if not row:
        raise ValueError(f"Label '{label}' not found in report.")
    return row.find_next_sibling('td').text.strip()

# Extract metrics
response_time = extract_metric("Average Response Time")
total_requests = extract_metric("Total Requests")
failures = extract_metric("Failures")

success_rate = (1 - float(failures) / float(total_requests)) * 100 if float(total_requests) else 100

def add_summary_line(label, value):
    p = soup.new_tag('p')
    strong = soup.new_tag('strong')
    strong.string = f'{label}: '
    p.append(strong)
    p.append(str(value))
    summary_section.append(p)

add_summary_line('Average Response Time', f'{response_time} ms')
add_summary_line('Total Requests', total_requests)
add_summary_line('Total Failures', failures)
add_summary_line('Success Rate', f'{success_rate:.2f}%')

soup.body.insert(0, summary_section)

with open('locust_report_customized.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))
from bs4 import BeautifulSoup

# Load the original HTML report
with open('locust_report.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Add custom CSS link to HTML head
css_link = soup.new_tag('link', rel='stylesheet', href='/tmp/styles/custom_style.css')
soup.head.append(css_link)

# Create summary section
summary_section = soup.new_tag('div', attrs={'class': 'summary-section'})

# Create and append the header
header = soup.new_tag('h1')
header.string = 'Load Test Summary'
summary_section.append(header)

# Fetch key data
response_time = soup.find(string="Average Response Time").find_next('td').text
total_requests = soup.find(string="Total Requests").find_next('td').text
failures = soup.find(string="Failures").find_next('td').text
success_rate = (1 - float(failures) / float(total_requests)) * 100 if float(total_requests) else 100


# Helper to create and append <p> tags
def add_summary_line(label, value):
    p = soup.new_tag('p')
    strong = soup.new_tag('strong')
    strong.string = f'{label}: '
    p.append(strong)
    p.append(str(value))
    summary_section.append(p)


add_summary_line('Average Response Time', f'{response_time} ms')
add_summary_line('Total Requests', total_requests)
add_summary_line('Total Failures', failures)
add_summary_line('Success Rate', f'{success_rate:.2f}%')

# Insert summary at the top of <body>
soup.body.insert(0, summary_section)

# Save the updated report
with open('locust_report_customized.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))
