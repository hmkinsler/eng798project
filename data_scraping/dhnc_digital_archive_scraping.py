import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
# from google.colab import files # this line is for Google Colab only

def scrape_page(url):
    """
    Extracts metadata fields from NCDCR pages
    """
    # Initialize with empty strings
    data = {
        'Title': '',
        'Date': '',
        'Creator': '',
        'Place': '',
        'MARS ID': '',
        'Description': '',
        'Subject': '',
        'Format': '',
        'URL': url,
        'Hyperlink': f'=HYPERLINK("{url}","View Item")'
    }

    # Get the page
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return data

    # Parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract title from page title
    if soup.title:
        title = soup.title.text.split(' - ')[0].strip()
        data['Title'] = title

    # Extract metadata from JavaScript variables
    for script in soup.find_all('script'):
        if script.string and 'parentInfo' in script.string:
            # Extract parentInfo object using regex
            match = re.search(r'parentInfo\s*=\s*({[^;]*});', script.string)
            if match:
                try:
                    # Extract metadata directly using regex
                    info_str = match.group(1)
                    metadata_match = re.search(r'allMetadata:\s*(\[.*?\]),\s*title', info_str, re.DOTALL)

                    if metadata_match:
                        metadata_str = metadata_match.group(1)

                        # Extract each field value individually
                        # For Date
                        date_match = re.search(r'"name":"Date".*?"value":"([^"]*)"', metadata_str)
                        if date_match and date_match.group(1):
                            data['Date'] = date_match.group(1)

                        # For Description
                        desc_match = re.search(r'"name":"Description".*?"value":"([^"]*)"', metadata_str)
                        if desc_match and desc_match.group(1):
                            data['Description'] = desc_match.group(1)

                        # For MARS ID
                        mars_match = re.search(r'"name":"MARS ID".*?"value":"([^"]*)"', metadata_str)
                        if mars_match and mars_match.group(1):
                            data['MARS ID'] = mars_match.group(1)

                        # For Creator - need to extract from tags array
                        creator_match = re.search(r'"name":"Creator".*?"tags":\[(.*?)\]', metadata_str)
                        if creator_match:
                            # Extract values from the tags array
                            creators = re.findall(r'"([^"]+)"', creator_match.group(1))
                            if creators:
                                data['Creator'] = ', '.join(creators)

                        # For Place
                        place_match = re.search(r'"name":"Place".*?"tags":\[(.*?)\]', metadata_str)
                        if place_match:
                            places = re.findall(r'"([^"]+)"', place_match.group(1))
                            if places:
                                data['Place'] = ', '.join(places)

                        # For Subject
                        subject_match = re.search(r'"name":"Subject".*?"tags":\[(.*?)\]', metadata_str)
                        if subject_match:
                            subjects = re.findall(r'"([^"]+)"', subject_match.group(1))
                            if subjects:
                                data['Subject'] = ', '.join(subjects)

                        # For Format
                        format_match = re.search(r'"name":"Format".*?"tags":\[(.*?)\]', metadata_str)
                        if format_match:
                            formats = re.findall(r'"([^"]+)"', format_match.group(1))
                            if formats:
                                data['Format'] = ', '.join(formats)
                except Exception as e:
                    print(f"Error parsing metadata: {e}")

    return data

urls = [
    "https://digital.ncdcr.gov/Documents/Detail/letter-albert-d.-grauer-and-paula-m.-grauer-to-gov.-dan-k.-moore-april-5-1968/273697",
"https://digital.ncdcr.gov/Documents/Detail/letter-albert-w.-grauer-and-norma-j.-grauer-to-gov.-dan-k.-moore-april-8-1968/273700",
"https://digital.ncdcr.gov/Documents/Detail/letter-alice-h.-estes-to-gov.-dan-k.-moore-april-7-1968/273628",
"https://digital.ncdcr.gov/Documents/Detail/letter-allen-wannamaker-to-gov.-dan-k.-moore-april-11-1968/274233",
"https://digital.ncdcr.gov/Documents/Detail/letter-c.-peter-setzer-to-governor-dan-k.-moore-may-3-1968/272624",
"https://digital.ncdcr.gov/Documents/Detail/letter-c.-s.-alexander-to-honorable-william-b.-umstead-july-12-1954/272877",
"https://digital.ncdcr.gov/Documents/Detail/letter-charles-c.-sharpe-iii-to-gov.-dan-k.-moore-april-7-1968/274119",
"https://digital.ncdcr.gov/Documents/Detail/letter-charles-dunn-to-t.-c.-jervay-editor-of-the-wilmington-journal-april-22-1968/273563",
"https://digital.ncdcr.gov/Documents/Detail/letter-charles-l.-cherry-to-gov.-dan-k.-moore-april-8-1968/273166",
"https://digital.ncdcr.gov/Documents/Detail/letter-clarence-w.-bailey-to-honorable-william-b.-umstead-october-31-1954/272902",
"https://digital.ncdcr.gov/Documents/Detail/letter-clayton-e.-heffner-jr.-to-gov.-dan-k.-moore-april-9-1968/273712",
"https://digital.ncdcr.gov/Documents/Detail/letter-clifton-m.-craig-to-county-director-of-social-services-revised-draft-september-30-1969/274276",
"https://digital.ncdcr.gov/Documents/Detail/letter-colonel-james-h.-mcclurkin-to-gov.-dan-k.-moore-april-26-1968/273895",
"https://digital.ncdcr.gov/Documents/Detail/letter-david-w.-stith-to-gov.-dan-k.-moore-february-21-1968/274148",
"https://digital.ncdcr.gov/Documents/Detail/letter-dorothy-e.-berry-to-governor-william-umstead-june-2-1954/272911",
"https://digital.ncdcr.gov/Documents/Detail/letter-dr.-o.-l.-sherrill-to-gov.-dan-k.-moore-april-18-1968/274123",
"https://digital.ncdcr.gov/Documents/Detail/letter-elder-stephen-p.-frink-to-gov.-dan-k.-moore-april-13-1968/273641",
"https://digital.ncdcr.gov/Documents/Detail/letter-eloise-severinson-to-colonel-clifton-m.-craig-july-25-1969/274284",
"https://digital.ncdcr.gov/Documents/Detail/letter-esther-seay-to-gov.-dan-k.-moore-april-16-1968/274100",
"https://digital.ncdcr.gov/Documents/Detail/letter-executive-board-lakeview-naacp-to-governor-dan-moore-december-9-1965/272656",
"https://digital.ncdcr.gov/Documents/Detail/letter-g.-alvin-tucker-to-gov.-dan-k.-moore-april-5-1968/274226",
"https://digital.ncdcr.gov/Documents/Detail/letter-gordon-o.-hinson-to-honorable-dan-k.-moore-september-7-1965/272634",
"https://digital.ncdcr.gov/Documents/Detail/letter-harry-mcmullan-attorney-general-to-honorable-william-b.-umstead-may-25-1954/272909",
"https://digital.ncdcr.gov/Documents/Detail/letter-homer-cannon-to-gov.-dan-k.-moore-april-5-1968/273105",
"https://digital.ncdcr.gov/Documents/Detail/letter-j.-h.-wheeler-to-the-honorable-luther-h.-hodges-february-12-1960/272570",
"https://digital.ncdcr.gov/Documents/Detail/letter-j.-w.-duffield-to-gov.-dan-k.-moore-july-26-1968/273551",
"https://digital.ncdcr.gov/Documents/Detail/letter-james-h.-glenn-to-gov.-dan-k.-moore-april-9-1968/273686",
"https://digital.ncdcr.gov/Documents/Detail/letter-jane-l.-knight-to-gov.-dan-k.-moore-april-10-1968/273847",
"https://digital.ncdcr.gov/Documents/Detail/letter-john-t.-caldwell-to-gov.-dan-k.-moore-regarding-dr.-leonard-hausman-may-16-1968/273100",
"https://digital.ncdcr.gov/Documents/Detail/letter-john-w.-duffield-to-gov.-dan-k.-moore-april-10-1968/273534",
"https://digital.ncdcr.gov/Documents/Detail/letter-juanita-s.-hilton-to-senator-robert-c.-byrd-april-9-1968/273727",
"https://digital.ncdcr.gov/Documents/Detail/letter-kathleen-lindsay-to-governor-luther-h.-hodges-march-1-1960/272554",
"https://digital.ncdcr.gov/Documents/Detail/letter-kenneth-kramer-to-gov.-dan-k.-moore-april-5-1968/273856",
"https://digital.ncdcr.gov/Documents/Detail/letter-l.-e.-jarman-to-gov.-dan-k.-moore-april-10-1968/273778",
"https://digital.ncdcr.gov/Documents/Detail/letter-leah-summers-to-governor-scott-july-13-1971/272860",
"https://digital.ncdcr.gov/Documents/Detail/letter-leary-t.-colie-to-gov.-dan-k.-moore-april-8-1968/273491",
"https://digital.ncdcr.gov/Documents/Detail/letter-lucy-b.-miller-to-gov.-dan-k.-moore-april-7-1968/273956",
"https://digital.ncdcr.gov/Documents/Detail/letter-lura-k.-kester-to-gov.-dan-k.-moore-april-10-1968/273832",
"https://digital.ncdcr.gov/Documents/Detail/letter-mack-f.-bennett-to-gov.-dan-k.-moore-april-15-1968/273075",
"https://digital.ncdcr.gov/Documents/Detail/letter-major-general-claude-t.-bowers-to-gov.-dan-k.-moore-february-16-1968/273082",
"https://digital.ncdcr.gov/Documents/Detail/letter-mary-mills-to-gov.-dan-k.-moore-regarding-her-correspondence-with-senator-robert-f.-kennedy-july-2-1968/273976",
"https://digital.ncdcr.gov/Documents/Detail/letter-mayor-r.-w.-grabarek-to-gov.-dan-k.-moore-april-18-1968/273690",
"https://digital.ncdcr.gov/Documents/Detail/letter-michael-rulison-and-helen-rulison-to-gov.-dan-k.-moore-april-10-1968/274088",
"https://digital.ncdcr.gov/Documents/Detail/letter-mr.-and-mrs.-j.-e.-cannup-to-gov.-dan-k.-moore-april-11-1968/273110",
"https://digital.ncdcr.gov/Documents/Detail/letter-mrs.-c.-b.-smith-to-gov.-dan-k.-moore-april-14-1968/274131",
"https://digital.ncdcr.gov/Documents/Detail/letter-mrs.-c.-h.-reed-to-gov.-dan-k.-moore-march-30-1968/274049",
"https://digital.ncdcr.gov/Documents/Detail/letter-mrs.-donna-smith-to-the-honorable-warren-e.-burger-chief-justice-supreme-court-april-27-1971/272855",
"https://digital.ncdcr.gov/Documents/Detail/letter-mrs.-lucille-allen-to-hon.-william-b.-umstead-july-10-1954/272880",
"https://digital.ncdcr.gov/Documents/Detail/letter-mrs.-preston-andrews-jr.-to-governor-william-b.-umstead-may-29-1954/272894",
"https://digital.ncdcr.gov/Documents/Detail/letter-nancy-louise-ervin-to-gov.-dan-k.-moore-april-8-1968/273623",
"https://digital.ncdcr.gov/Documents/Detail/letter-okelley-whitaker-to-gov.-dan-k.-moore-april-10-1968/274250",
"https://digital.ncdcr.gov/Documents/Detail/letter-reverend-george-g.-higgins-to-gov.-dan-k.-moore-april-11-1968/273720",
"https://digital.ncdcr.gov/Documents/Detail/letter-reverend-julius-h.-corpening-to-gov.-dan-k.-moore-march-25-1968/273495",
"https://digital.ncdcr.gov/Documents/Detail/letter-reverend-l.-r.-mcknight-to-gov.-dan-k.-moore-september-29-1968/273908",
"https://digital.ncdcr.gov/Documents/Detail/letter-reverend-stephen-n.-levinson-to-gov.-dan-k.-moore-april-16-1968/273877",
"https://digital.ncdcr.gov/Documents/Detail/letter-sandra-porter-to-governor-luther-hodges-march-11-1960/272565",
"https://digital.ncdcr.gov/Documents/Detail/letter-thelma-howell-to-governor-luther-hodges-march-13-1960/272548",
"https://digital.ncdcr.gov/Documents/Detail/letter-virgil-hyman-to-gov.-dan-k.-moore-april-11-1968/273759",
"https://digital.ncdcr.gov/Documents/Detail/letter-walter-c.-daniel-to-gov.-dan-k.-moore-april-13-1968/273507",
"https://digital.ncdcr.gov/Documents/Detail/letter-wilfred-a.-wells-to-gov.-dan-k.-moore-april-18-1968/274239",
"https://digital.ncdcr.gov/Documents/Detail/letter-william-b.-umstead-to-mr.-kelly-m.-alexander-june-24-1954/272966",
"https://digital.ncdcr.gov/Documents/Detail/letter-william-c.-allred-jr.-to-the-honorable-luther-h.-hodges-march-11-1960/272541",
"https://digital.ncdcr.gov/Documents/Detail/letter-william-calvin-ijames-to-gov.-dan-k.-moore-april-13-1968/273762",
"https://digital.ncdcr.gov/Documents/Detail/letter-william-norris-to-gov.-dan-k.-moore-april-1968/274018",
"https://digital.ncdcr.gov/Documents/Detail/letter-wilson-w.-lee-to-gov.-dan-k.-moore-may-4-1968/273870",
"https://digital.ncdcr.gov/Documents/Detail/letter-wm.-e.-black-and-mrs.-w.-e.-agnes-black-to-governor-luther-hodges-february-4-1960/272543",
"https://digital.ncdcr.gov/Documents/Detail/letters-from-emily-w.-elmore-to-gov.-dan-k.-moore-march-23-april-24-and-april-29-1968/273576",
"https://digital.ncdcr.gov/Documents/Detail/letters-from-james-c.-gardner-to-gov.-dan-k.-moore-regarding-the-north-carolina-fund/273661",
"https://digital.ncdcr.gov/Documents/Detail/letters-from-montie-garry-pam-and-valma-bailey-to-gov.-dan-k.-moore-regarding-race-relations-and-african-american-rights-april-24-1968/273011",
"https://digital.ncdcr.gov/Documents/Detail/letters-protesting-the-appearance-of-stokely-carmichael-at-any-state-supported-institution/273117",
"https://digital.ncdcr.gov/Documents/Detail/letters-and-telegrams-regarding-the-protests-of-high-school-students-in-swanquarter-nc/2741"]

# For a single URL test
result = scrape_page(url)
print("Extracted metadata:")
for field, value in result.items():
    print(f"{field}: {value}")

# Create DataFrame with the results
df = pd.DataFrame([result])

# Save to Excel file
excel_file = 'ncdcr_data.xlsx'
df.to_excel(excel_file, index=False)
print(f"\nSaved data to {excel_file}")

# Download the Excel file
files.download(excel_file)
print(f"Downloaded {excel_file} - check your downloads folder")

# FOR MULTIPLE URLS:
# results = []
# for url in urls:
#     print(f"Processing: {url}")
#     data = scrape_page(url)
#     results.append(data)
#
# df = pd.DataFrame(results)
# excel_file = 'ncdcr_multiple_data.xlsx'
# df.to_excel(excel_file, index=False)
# files.download(excel_file)