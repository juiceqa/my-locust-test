from bs4 import BeautifulSoup

with open('locust_report.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Add custom CSS link
css_link = soup.new_tag('link', rel='stylesheet', href='/tmp/styles/custom_style.css')
soup.head.append(css_link)

# Create summary section
summary_section = soup.new_tag('div', attrs={'class': 'summary-section'})
header = soup.new_tag('h1')
header.string = 'Load Test Summary'
summary_section.append(header)

def extract_metric(label):
    """ Extract metric value based on label from the report. """
    row = soup.find('td', string=label)
    if not row:
        raise ValueError(f"Label '{label}' not found in report.")
    return row.find_next_sibling('td').text.strip()

def extract_average_response_time():
    """ Extract average response time from the 'Request Statistics' section. """
    request_stats_section = soup.find('h2', string="Request Statistics")
    if not request_stats_section:
        raise ValueError("Request Statistics section not found.")

    # Find the row containing 'Average (ms)' in the Request Statistics table
    average_row = request_stats_section.find_next('table').find('td', string="Average (ms)")
    if not average_row:
        raise ValueError("'Average (ms)' not found in the report.")

    return average_row.find_next_sibling('td').text.strip()

# Extract metrics
response_time = extract_average_response_time()
total_requests = extract_metric("Total Requests")
failures = extract_metric("Failures")

# Calculate success rate
success_rate = (1 - float(failures) / float(total_requests)) * 100 if float(total_requests) else 100

# Function to add summary lines
def add_summary_line(label, value):
    p = soup.new_tag('p')
    strong = soup.new_tag('strong')
    strong.string = f'{label}: '
    p.append(strong)
    p.append(str(value))
    summary_section.append(p)

# Add the summary lines to the summary section
add_summary_line('Average Response Time', f'{response_time} ms')
add_summary_line('Total Requests', total_requests)
add_summary_line('Total Failures', failures)
add_summary_line('Success Rate', f'{success_rate:.2f}%')

# Insert the summary section at the top of the report
soup.body.insert(0, summary_section)

# Save the modified report
with open('locust_report_customized.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

print("Custom report generated successfully.")
