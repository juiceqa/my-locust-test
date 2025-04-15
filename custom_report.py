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
    table_headers = [th.get_text(strip=True) for th in table.find_all("th")]
    try:
        idx = table_headers.index(column_name)
    except ValueError:
        return None
    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if cells and "Aggregated" in cells[0].text:
            return cells[idx].text.strip()
    return None


def add_summary_line(label, value):
    p = soup.new_tag('p')
    strong = soup.new_tag('strong')
    strong.string = f'{label}: '
    p.append(strong)
    p.append(str(value))
    summary_section.append(p)


req_stats = get_table_by_heading("Request Statistics")
avg_resp_time = get_aggregated_value(req_stats, "Average (ms)")
total_requests = get_aggregated_value(req_stats, "# Requests")
failures = get_aggregated_value(req_stats, "# Fails")
rps = get_aggregated_value(req_stats, "RPS")
failures_s = get_aggregated_value(req_stats, "Failures/s")

success_rate = (
    (1 - float(failures) / float(total_requests)) * 100
    if total_requests and float(total_requests) else 100
)

add_summary_line("Average Response Time", f"{avg_resp_time} ms")
add_summary_line("Total Requests", total_requests)
add_summary_line("Total Failures", failures)
add_summary_line("Requests per Second", rps)
add_summary_line("Failures per Second", failures_s)
add_summary_line("Success Rate", f"{success_rate:.2f}%")


# Percentiles
resp_table = get_table_by_heading("Response Time Statistics")
if resp_table:
    percent_headers = [th.get_text(strip=True) for th in resp_table.find_all("th")]
    agg_row = next((row for row in resp_table.find_all("tr") if "Aggregated" in row.get_text()), None)
    if agg_row:
        agg_cols = [td.get_text(strip=True) for td in agg_row.find_all("td")]
        add_summary_line("Response Time Percentiles", "")
        for i, col_name in enumerate(percent_headers[2:], start=2):
            add_summary_line(f"  {col_name}", f"{agg_cols[i]} ms")


# Failures
fail_section = soup.find("h2", string="Failures Statistics")
if fail_section:
    fail_table = fail_section.find_next("table")
    if fail_table:
        for row in fail_table.find_all("tr")[1:]:
            cells = row.find_all("td")
            if len(cells) >= 4:
                detail = (
                    f"{cells[0].text.strip()} failures — "
                    f"Method: {cells[1].text.strip()} | "
                    f"Name: {cells[2].text.strip()} | "
                    f"Error: {cells[3].text.strip()}"
                )
                add_summary_line("Failure Detail", detail)

# Finally, insert the summary at the top of the body or relevant container if needed
body_tag = soup.body or soup.find("div", {"id": "content"})
if body_tag:
    body_tag.insert(0, summary_section)

# Optionally write back to file
with open('locust_report_with_summary.html', 'w', encoding='utf-8') as file:
    file.write(str(soup.prettify()))
