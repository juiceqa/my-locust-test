from bs4 import BeautifulSoup

# Assuming `soup` is your BeautifulSoup object
# Add custom CSS link to HTML
css_link = soup.new_tag('link', rel='stylesheet', href='/tmp/styles/custom_style.css')
soup.head.append(css_link)

# Add summary section to the report
summary_section = soup.new_tag('div', attrs={'class': 'summary-section'})
summary_section.append('<h1>Load Test Summary</h1>')

# Fetching key data like average response time, failures, and success rate
response_time = soup.find(text="Average Response Time").find_next('td').text
total_requests = soup.find(text="Total Requests").find_next('td').text
failures = soup.find(text="Failures").find_next('td').text
success_rate = (1 - float(failures) / float(total_requests)) * 100 if total_requests else 100

# Add data to the summary section
summary_section.append(f'<p><strong>Average Response Time: </strong>{response_time} ms</p>')
summary_section.append(f'<p><strong>Total Requests: </strong>{total_requests}</p>')
summary_section.append(f'<p><strong>Total Failures: </strong>{failures}</p>')
summary_section.append(f'<p><strong>Success Rate: </strong>{success_rate:.2f}%</p>')

# Insert this summary into the report
soup.body.insert(0, summary_section)

# Save the customized report
with open('locust_report_customized.html', 'w') as file:
    file.write(str(soup))
