from bs4 import BeautifulSoup

with open('locust_report.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

summary_section = soup.new_tag('div', attrs={'class': 'summary-section'})
header = soup.new_tag('h1')
header.string = 'Load Test Summary'
summary_section.append(header)

def get_table_by_heading(heading_text):
    heading = soup.find("h2", string=heading_text)
    return heading.find_next("table") if heading else None

def get_aggregated_value(table, column_name):
    if not table:
        return None
    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    try:
        index = headers.index(column_name)
    except ValueError:
        return None
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if cols and "Aggregated" in cols[0].text:
            return cols[index].text.strip()
    return None

def add_summary_line(label, value):
    p = soup.new_tag('p')
    strong = soup.new_tag('strong')
    strong.string = f'{label}: '
    p.append(strong)
    p.append(str(value))
    summary_section.append(p)

# Request Stats
req_stats = get_table_by_heading("Request Statistics")
avg_resp_time = get_aggregated_value(req_stats, "Average (ms)")
total_requests = get_aggregated_value(req_stats, "# Requests")
failures = get_aggregated_value(req_stats, "# Fails")
rps = get_aggregated_value(req_stats, "RPS")
failures_s = get_aggregated_value(req_stats, "Failures/s")

success_rate = (1 - float(failures) / float(total_requests)) * 100 if total_requests and float(total_requests) else 100

add_summary_line("Average Response Time", f"{avg_resp_time} ms")
add_summary_line("Total Requests", total_requests)
add_summary_line("Total Failures", failures)
add_summary_line("Requests per Second", rps)
add_summary_line("Failures per Second", failures_s)
add_summary_line("Success Rate", f"{success_rate:.2f}%")

# Response Time Statistics
resp_table = get_table_by_heading("Response Time Statistics")
if resp_table:
    headers = [th.get_text(strip=True) for th in resp_table.find_all("th")]
    agg_row = next((tr for tr in resp_table.find_all("tr") if "Aggregated" in tr.get_text()), None)
    if agg_row:
        cols = [td.get_text(strip=True) for td in agg_row.find_all("td")]
        add_summary_line("Response Time Percentiles", "")
        for label in headers[2:]:
            value = cols[headers.index(label)]
            add_summary_line(f"  {label}", f"{value} ms")

# Failures
fail_table = get_table_by_heading("Failures Statistics")
fail_rows = fail_table.find_all("tr")[1:] if fail_table else []
if fail_rows:
    fail_header = soup.new_tag("h2")
    fail_header.string = "Failure Details"
    summary_section.append(fail_header)
    for row in fail_rows:
        cols = row.find_all("td")
        if len(cols) >= 4:
            detail = f"{cols[1].text.strip()} {cols[2].text.strip()} — {cols[3].text.strip()} ({cols[0].text.strip()} times)"
            p = soup.new_tag("p")
            p.string = detail
            summary_section.append(p)

# Final Ratio Section
ratio_header = soup.find("h2", string="Final ratio")
if ratio_header:
    p_tags = ratio_header.find_all_next("p")
    ratio_lines = []
    for p in p_tags:
        if p.find("strong"):  # stop if hitting another section
            break
        text = p.get_text(strip=True)
        if "%" in text and any(c.isalpha() for c in text):  # likely a class label
            ratio_lines.append(text)
    if ratio_lines:
        section = soup.new_tag("div")
        sub_header = soup.new_tag("h2")
        sub_header.string = "Final Ratio"
        section.append(sub_header)
        for line in ratio_lines:
            p = soup.new_tag("p")
            p.string = line
            section.append(p)
        summary_section.append(section)

soup.body.insert(0, summary_section)

with open('locust_report_customized.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))
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
from bs4 import BeautifulSoup

with open('locust_report.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

summary_section = soup.new_tag('div', attrs={'class': 'summary-section'})
header = soup.new_tag('h1')
header.string = 'Load Test Summary'
summary_section.append(header)

def get_table_by_heading(heading_text):
    heading = soup.find("h2", string=heading_text)
    return heading.find_next("table") if heading else None

def get_aggregated_value(table, column_name):
    if not table:
        return None
    headers = [th.get_text(strip=True) for th in table.find_all("th")]
    try:
        index = headers.index(column_name)
    except ValueError:
        return None
    for row in table.find_all("tr"):
        cols = row.find_all("td")
        if cols and "Aggregated" in cols[0].text:
            return cols[index].text.strip()
    return None

def add_summary_line(label, value):
    p = soup.new_tag('p')
    strong = soup.new_tag('strong')
    strong.string = f'{label}: '
    p.append(strong)
    p.append(str(value))
    summary_section.append(p)

# Request Stats
req_stats = get_table_by_heading("Request Statistics")
avg_resp_time = get_aggregated_value(req_stats, "Average (ms)")
total_requests = get_aggregated_value(req_stats, "# Requests")
failures = get_aggregated_value(req_stats, "# Fails")
rps = get_aggregated_value(req_stats, "RPS")
failures_s = get_aggregated_value(req_stats, "Failures/s")

success_rate = (1 - float(failures) / float(total_requests)) * 100 if total_requests and float(total_requests) else 100

add_summary_line("Average Response Time", f"{avg_resp_time} ms")
add_summary_line("Total Requests", total_requests)
add_summary_line("Total Failures", failures)
add_summary_line("Requests per Second", rps)
add_summary_line("Failures per Second", failures_s)
add_summary_line("Success Rate", f"{success_rate:.2f}%")

# Response Time Statistics
resp_table = get_table_by_heading("Response Time Statistics")
if resp_table:
    headers = [th.get_text(strip=True) for th in resp_table.find_all("th")]
    agg_row = next((tr for tr in resp_table.find_all("tr") if "Aggregated" in tr.get_text()), None)
    if agg_row:
        cols = [td.get_text(strip=True) for td in agg_row.find_all("td")]
        add_summary_line("Response Time Percentiles", "")
        for label in headers[2:]:
            value = cols[headers.index(label)]
            add_summary_line(f"  {label}", f"{value} ms")

# Failures
fail_table = get_table_by_heading("Failures Statistics")
fail_rows = fail_table.find_all("tr")[1:] if fail_table else []
if fail_rows:
    fail_header = soup.new_tag("h2")
    fail_header.string = "Failure Details"
    summary_section.append(fail_header)
    for row in fail_rows:
        cols = row.find_all("td")
        if len(cols) >= 4:
            detail = f"{cols[1].text.strip()} {cols[2].text.strip()} — {cols[3].text.strip()} ({cols[0].text.strip()} times)"
            p = soup.new_tag("p")
            p.string = detail
            summary_section.append(p)

# Final Ratio Section
ratio_header = soup.find("h2", string="Final ratio")
if ratio_header:
    p_tags = ratio_header.find_all_next("p")
    ratio_lines = []
    for p in p_tags:
        if p.find("strong"):  # stop if hitting another section
            break
        text = p.get_text(strip=True)
        if "%" in text and any(c.isalpha() for c in text):  # likely a class label
            ratio_lines.append(text)
    if ratio_lines:
        section = soup.new_tag("div")
        sub_header = soup.new_tag("h2")
        sub_header.string = "Final Ratio"
        section.append(sub_header)
        for line in ratio_lines:
            p = soup.new_tag("p")
            p.string = line
            section.append(p)
        summary_section.append(section)

soup.body.insert(0, summary_section)

with open('locust_report_customized.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

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
