from bs4 import BeautifulSoup

with open('locust_report.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Create a new summary section for the report
summary_section = soup.new_tag('div', attrs={'class': 'summary-section'})
header = soup.new_tag('h1')
header.string = 'Load Test Summary'
summary_section.append(header)

def get_table_by_heading(heading_text):
    # Locate the table by the heading text
    heading = soup.find("h2", string=heading_text)
    return heading.find_next("table") if heading else None

def get_aggregated_value(table, column_name):
    # Get aggregated values from the table based on column headers
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
    # Add a line to the summary section
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

# Calculate success rate
success_rate = (1 - float(failures) / float(total_requests)) * 100 if total_requests and float(total_requests) else 100

# Add these values to the summary section
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

# Failures Section (Updated)
fail_section = soup.find("h2", string="Failures Statistics")
if fail_section:
    fail_table = fail_section.find_next("table")
    if fail_table:
        failure_details = []
        for row in fail_table.find_all("tr")[1:]:  # skip the header row
            cols = row.find_all("td")
            if len(cols) >= 4:
                # Extract failure details: occurrences, method, name, error message
                detail = f"{cols[0].text.strip()} failures — Method: {cols[1].text.strip()} | Name: {cols[2].text.strip()} | Error: {cols[3].text.strip()}"
                failure_details.append(detail)

        if failure_details:
            fail_header = soup.new_tag("h2")
            fail_header.string = "Failure Details"
            summary_section.append(fail_header)
            for detail in failure_details:
                p = soup.new_tag("p")
                p.string = detail
                summary_section.append(p)

# Final Ratio Section (Updated)
final_ratio_section = soup.find("h2", string="Final ratio")
if final_ratio_section:
    # Extract "Ratio Per Class" and "Total Ratio" sections
    ratio_details = []
    ratio_per_class_section = final_ratio_section.find_next("h3", string="Ratio Per Class")
    if ratio_per_class_section:
        class_items = ratio_per_class_section.find_next("ul").find_all("li")
        for item in class_items:
            class_name = item.find("ul").previous_sibling.strip() if item.find("ul") else item.get_text(strip=True)
            sub_items = item.find_all("li")
            for sub_item in sub_items:
                ratio_details.append(f"  {sub_item.get_text(strip=True)} under class {class_name}")

    total_ratio_section = final_ratio_section.find_next("h3", string="Total Ratio")
    if total_ratio_section:
        class_items = total_ratio_section.find_next("ul").find_all("li")
        for item in class_items:
            class_name = item.find("ul").previous_sibling.strip() if item.find("ul") else item.get_text(strip=True)
            sub_items = item.find_all("li")
            for sub_item in sub_items:
                ratio_details.append(f"  {sub_item.get_text(strip=True)} under class {class_name}")

    # Add the final ratio details to the summary section
    if ratio_details:
        ratio_header = soup.new_tag("h2")
        ratio_header.string = "Final Ratio Details"
        summary_section.append(ratio_header)
        for detail in ratio_details:
            p = soup.new_tag("p")
            p.string = detail
            summary_section.append(p)

# Charts Section (Updated)
chart_section = soup.find("h2", string="Charts")
if chart_section:
    # Extract chart data from the chart divs
    chart_details = []
    chart_divs = chart_section.find_all_next("div", {"_echarts_instance_": True})
    for chart in chart_divs:
        tooltip = chart.find("div", {"style": "position: absolute;"})
        if tooltip:
            tooltip_text = tooltip.get_text(strip=True)
            # Extract relevant data from tooltip text
            if 'RPS' in tooltip_text:
                rps_value = tooltip_text.split('RPS:')[1].split()[0]
                chart_details.append(f"RPS: {rps_value}")
            if 'Failures/s' in tooltip_text:
                failures_s_value = tooltip_text.split('Failures/s:')[1].split()[0]
                chart_details.append(f"Failures per Second: {failures_s_value}")
            if '50th percentile' in tooltip_text:
                p50_value = tooltip_text.split('50th percentile:')[1].split()[0]
                chart_details.append(f"50th Percentile: {p50_value} ms")
            if '95th percentile' in tooltip_text:
                p95_value = tooltip_text.split('95th percentile:')[1].split()[0]
                chart_details.append(f"95th Percentile: {p95_value} ms")
            if 'Number of Users' in tooltip_text:
                num_users = tooltip_text.split('Number of Users:')[1].split()[0]
                chart_details.append(f"Number of Users: {num_users}")

    # Add chart details to the summary
    if chart_details:
        chart_header = soup.new_tag("h2")
        chart_header.string = "Chart Details"
        summary_section.append(chart_header)
        for detail in chart_details:
            p = soup.new_tag("p")
            p.string = detail
            summary_section.append(p)

# Insert the summary section at the beginning of the body
soup.body.insert(0, summary_section)

# Write the customized report to a new file
with open('locust_report_customized.html', 'w', encoding='utf-8') as file:
    file.write(str(soup))

print("Report generated successfully as 'locust_report_customized.html'")
