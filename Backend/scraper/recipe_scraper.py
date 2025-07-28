import requests
from bs4 import BeautifulSoup
import json
import xml.etree.ElementTree as ET
from xml.dom import minidom
import re
import os
import sys
from datetime import datetime
from lxml import etree
import csv

from .data_save_mysql import insert_recipe_from_xml as insert_recipe_from_xml

def scrape_sitemap_urls(url):
    """
    Scrapes URLs from a sitemap (remains synchronous as it's a quick, initial step).
    """
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        print(f"Fetching sitemap from: {url}")
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        content_type = response.headers.get('content-type', '').lower()
        urls = []
        if 'xml' in content_type or url.endswith('.xml'):
            try:
                root = ET.fromstring(response.content)
                namespaces = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
                url_elements = root.findall('.//sitemap:url', namespaces)
                if not url_elements:
                    url_elements = root.findall('.//url')
                for url_elem in url_elements:
                    loc_elem = url_elem.find('sitemap:loc', namespaces)
                    if loc_elem is None:
                        loc_elem = url_elem.find('loc')
                    if loc_elem is not None and loc_elem.text:
                        urls.append(loc_elem.text.strip())
            except ET.ParseError:
                urls = parse_html_sitemap(response.content)
        else:
            urls = parse_html_sitemap(response.content)
        print(f"Found {len(urls)} URLs.")
        return urls
    except requests.RequestException as e:
        print(f"Error fetching sitemap: {e}")
        return []
    except Exception as e:
        print(f"Error parsing sitemap: {e}")
        return []

def parse_html_sitemap(content):
    """
    Parses an HTML-formatted sitemap.
    """
    urls = []
    soup = BeautifulSoup(content, 'html.parser')
    sitemap_table = soup.find('table', {'id': 'sitemap'})
    if not sitemap_table:
        return []
    tbody = sitemap_table.find('tbody')
    if tbody:
        for row in tbody.find_all('tr'):
            link = row.find('a')
            if link and link.get('href'):
                urls.append(link.get('href'))
    return urls

def parse_recipe_content(html_content, url):
    """
    Parses the HTML content of a recipe page to extract data.
    This function no longer performs the request itself.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    recipe_data = {
        "url": url,
        "scraped_time": datetime.now().isoformat(),
        "recipe_name": "", "picture_url": "", "cuisine": "", "time": "",
        "ingredients": [], "directions": [],
        "nutrition_facts_per_serving": {"calories": "", "fat": "", "carbs": "", "protein": "", "sugar": ""}
    }

    # --- All the detailed parsing logic remains exactly the same ---
    name_elem = soup.select_one('.tasty-recipeResults-title, .wprm-recipe-name, h1[itemprop="name"]')
    if name_elem:
        recipe_data["recipe_name"] = name_elem.get_text(strip=True)
    image_elem = soup.select_one('figure.wp-block-image img, .tasty-recipeResults-image img, .wprm-recipe-image img')
    if image_elem and image_elem.has_attr('src'):
        recipe_data["picture_url"] = image_elem['src']
    cuisine_elem = soup.select_one('span.tasty-recipeResults-cuisine')
    if cuisine_elem:
        recipe_data["cuisine"] = cuisine_elem.get_text(strip=True)
    time_elem = soup.select_one('.tasty-recipeResults-total-time, .wprm-recipe-total_time-container .wprm-recipe-time, [itemprop="totalTime"]')
    if time_elem:
        recipe_data["time"] = time_elem.get_text(strip=True)
    parsed_ingredients_from_html = []
    ingredient_elems_html = soup.select('li[data-tr-ingredient-checkbox], .tasty-recipeResults-ingredients-body li, .wprm-recipe-ingredient')
    for li in ingredient_elems_html:
        full_text = li.get_text(separator=' ', strip=True)
        if not full_text: continue
        parsed_result = parse_ingredient(full_text)
        ingredient_amount = parsed_result.get('amount', '')
        ingredient_name = parsed_result.get('name', '')
        strong_tags = li.find_all('strong')
        if strong_tags:
            candidate_strong_name = strong_tags[-1].get_text(strip=True)
            units_for_check = ('cup','cups','c','tablespoon','tablespoons','tbsp','teaspoon','teaspoons','tsp','pound','pounds','lb','lbs','ounce','ounces','oz','gram','grams','g','kg','clove','cloves','can','cans','jar','jars','package','packages','pinch','slice','slices','head','heads','sprig','sprigs','bunch','bunches','piece','pieces','egg','eggs','fillet','fillets','stalk','stalks','sheet','sheets','leaf','leaves','sprinkle','sprinkles','pint','pints','quart','quarts','gallon','gallons','liter','liters','ml','dash','dashes','fl.oz','fl oz','oz.','doz','dozen','box','boxes','bag','bags','container','containers','bottle','bottles','strip','strips','wedge','wedges','ear','ears')
            units_pattern_for_check = r'(?:' + '|'.join(re.escape(u) for u in units_for_check) + r')'
            if not (re.fullmatch(r'^\s*(\d+(?:[\s\/\.-]\d+)?)\s*(?:' + units_pattern_for_check + r')?s?\s*$', candidate_strong_name, re.IGNORECASE) or re.fullmatch(r'^\s*(?:a|an|one|two|three|four|five|six|seven|eight|nine|ten)\s*(?:' + units_pattern_for_check + r')?s?\s*$', candidate_strong_name, re.IGNORECASE)):
                if candidate_strong_name in ingredient_name:
                    ingredient_name = candidate_strong_name
        if "salt and pepper" in full_text.lower():
            if "salt and pepper" in ingredient_name.lower(): pass
            elif ingredient_name.lower() in ("pepper", "salt", "salt pepper"): ingredient_name = "salt and pepper"
            amount_match_for_salt_pepper = re.match(r'^\s*(\d+(?:[\s\/\.-]\d+)?\s*(?:teaspoon|tsp)?s?)\s*(?:of\s*)?salt(?:(?:\s*and\s*)?pepper)?\b', full_text, re.IGNORECASE)
            if amount_match_for_salt_pepper: ingredient_amount = amount_match_for_salt_pepper.group(1).strip()
            elif "to taste" in full_text.lower() and not ingredient_amount: ingredient_amount = "to taste"
        if ingredient_name or ingredient_amount:
            parsed_ingredients_from_html.append({"amount": ingredient_amount, "name": ingredient_name})
    recipe_data["ingredients"] = parsed_ingredients_from_html
    direction_elems_html = soup.select('.tasty-recipeResults-instructions-body li, .wprm-recipe-instruction-text, .tasty-recipeResults-instructions li, [itemprop="recipeInstructions"] li, [itemprop="recipeInstructions"] p')
    recipe_data["directions"] = [d.get_text(strip=True) for d in direction_elems_html if d.get_text(strip=True)]
    nutrition_elems_html = soup.select('.tasty-recipeResults-nutrition li, .wprm-nutrition-label-container span, .tasty-recipeResults-nutrition-details span, [itemprop="nutrition"] [itemprop]')
    for elem in nutrition_elems_html:
        text = elem.get_text(strip=True).lower()
        if elem.get('itemprop') == 'calories' and elem.get_text(strip=True): recipe_data["nutrition_facts_per_serving"]["calories"] = elem.get_text(strip=True)
        elif elem.get('itemprop') == 'fatContent' and elem.get_text(strip=True): recipe_data["nutrition_facts_per_serving"]["fat"] = elem.get_text(strip=True)
        elif elem.get('itemprop') == 'carbohydrateContent' and elem.get_text(strip=True): recipe_data["nutrition_facts_per_serving"]["carbs"] = elem.get_text(strip=True)
        elif elem.get('itemprop') == 'proteinContent' and elem.get_text(strip=True): recipe_data["nutrition_facts_per_serving"]["protein"] = elem.get_text(strip=True)
        elif elem.get('itemprop') == 'sugarContent' and elem.get_text(strip=True): recipe_data["nutrition_facts_per_serving"]["sugar"] = elem.get_text(strip=True)
        elif "calories" in text and not recipe_data["nutrition_facts_per_serving"]["calories"]:
            match = re.search(r'calories:\s*([\d.]+)', text)
            if match: recipe_data["nutrition_facts_per_serving"]["calories"] = match.group(1) + " calories"
        elif "fat" in text and not recipe_data["nutrition_facts_per_serving"]["fat"]:
            match = re.search(r'fat:\s*([\d.]+)', text)
            if match: recipe_data["nutrition_facts_per_serving"]["fat"] = match.group(1) + " g"
        elif ("carbohydrates" in text or "carbs" in text) and not recipe_data["nutrition_facts_per_serving"]["carbs"]:
            match = re.search(r'(?:carbohydrates|carbs):\s*([\d.]+)', text)
            if match: recipe_data["nutrition_facts_per_serving"]["carbs"] = match.group(1) + " g"
        elif "protein" in text and not recipe_data["nutrition_facts_per_serving"]["protein"]:
            match = re.search(r'protein:\s*([\d.]+)', text)
            if match: recipe_data["nutrition_facts_per_serving"]["protein"] = match.group(1) + " g"
        elif "sugar" in text and not recipe_data["nutrition_facts_per_serving"]["sugar"]:
            match = re.search(r'sugar:\s*([\d.]+)', text)
            if match: recipe_data["nutrition_facts_per_serving"]["sugar"] = match.group(1) + " g"
    json_ld_scripts = soup.find_all('script', type='application/ld+json')
    recipe_json = None
    for script in json_ld_scripts:
        try:
            data = json.loads(script.string)
            if '@graph' in data:
                for item in data.get('@graph', []):
                    if item.get('@type') == 'Recipe': recipe_json = item; break
            if not recipe_json and data.get('@type') == 'Recipe': recipe_json = data
            if not recipe_json and isinstance(data, list):
                for item in data:
                    if item.get('@type') == 'Recipe': recipe_json = item; break
            if recipe_json: break
        except json.JSONDecodeError: continue
    if recipe_json:
        if all(not val for val in recipe_data["nutrition_facts_per_serving"].values()) and recipe_json.get('nutrition'):
            nutrition = recipe_json['nutrition']
            recipe_data["nutrition_facts_per_serving"] = {"calories": str(nutrition.get('calories', '')),"fat": str(nutrition.get('fatContent', '')),"carbs": str(nutrition.get('carbohydrateContent', '')),"protein": str(nutrition.get('proteinContent', '')),"sugar": str(nutrition.get('sugarContent', ''))}
    return recipe_data

def parse_ingredient(text):
    text = text.strip().replace('½', '1/2').replace('¼', '1/4').replace('¾', '3/4').replace('–', '-').replace('—', '-').replace('\u2013', '-').replace('\u2014', '-')
    cleaned_text = re.sub(r'\s*\([^)]*\)', '', text).strip()
    units_raw = ('teaspoon','tablespoon','tbsp','tsp','cup','c','pound','lb','lbs','ounce','oz','gram','g','kg','clove','can','jar','package','pinch','slice','head','sprig','bunch','piece','egg','fillet','stalk','sheet','leaf','sprinkle','pint','quart','gallon','liter','ml','dash','fl.oz','fl oz','oz.','doz','dozen','box','bag','container','bottle','strip','wedge','ear')
    units_pattern = r'\b(?:' + '|'.join(re.escape(u) for u in units_raw) + r')s?\b'
    amount_regex = re.compile(r'^\s*((?:(?:a|an|one|two|three|four|five|six|seven|eight|nine|ten|[0-9\s\/\.-]+)\s*)+(?:' + units_pattern + r')?\.?)\s*', re.IGNORECASE)
    match = amount_regex.match(cleaned_text)
    amount, name = "", cleaned_text
    if match:
        potential_amount = match.group(1).strip()
        if any(char.isdigit() for char in potential_amount) or re.search(units_pattern, potential_amount, re.IGNORECASE):
            amount = potential_amount
            name = cleaned_text[match.end():].strip()
    if ',' in name: name = name.split(',')[0].strip()
    if name.lower().startswith('of '): name = name[3:].strip()
    amount = re.sub(r'\s+of\s*$', '', amount, flags=re.IGNORECASE).strip()
    if not name and amount:
        parts = amount.split()
        if not parts[-1].isdigit() and not re.search(units_pattern, parts[-1], re.IGNORECASE):
            name = parts.pop()
            amount = " ".join(parts)
    return {"amount": amount, "name": name}

def create_xml(recipe_data):
    root = ET.Element("recipe")
    ET.SubElement(root, "url").text = recipe_data.get("url", "")
    ET.SubElement(root, "scraped_time").text = recipe_data.get("scraped_time", "")
    ET.SubElement(root, "recipe_name").text = recipe_data.get("recipe_name", "")
    ET.SubElement(root, "picture_url").text = recipe_data.get("picture_url", "")
    ET.SubElement(root, "cuisine").text = recipe_data.get("cuisine", "")
    ET.SubElement(root, "time").text = recipe_data.get("time", "")
    ingredients_elem = ET.SubElement(root, "ingredients")
    if recipe_data.get("ingredients"):
        for ingredient in recipe_data.get("ingredients"):
            ing_elem = ET.SubElement(ingredients_elem, "ingredient")
            ET.SubElement(ing_elem, "amount").text = ingredient.get("amount", "")
            ET.SubElement(ing_elem, "name").text = ingredient.get("name", "")
    directions_elem = ET.SubElement(root, "directions")
    if recipe_data.get("directions"):
        for direction in recipe_data.get("directions"):
            ET.SubElement(directions_elem, "direction").text = direction
    nutrition_elem = ET.SubElement(root, "nutrition_facts_per_serving")
    if recipe_data.get("nutrition_facts_per_serving"):
        for key, value in recipe_data["nutrition_facts_per_serving"].items():
            ET.SubElement(nutrition_elem, key).text = str(value)
    rough_string = ET.tostring(root, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

def validate_xml(xml_file_path, rng_file_path):
    """
    Validates an XML file against a RelaxNG schema.
    """
    try:
        rng_doc = etree.parse(rng_file_path)
        rng_schema = etree.RelaxNG(rng_doc)
        xml_doc = etree.parse(xml_file_path)
        rng_schema.assertValid(xml_doc)
        return True, None
    except etree.XMLSyntaxError as e:
        return False, f"XML Syntax Error: {e}"
    except etree.DocumentInvalid as e:
        errors = "\n".join([str(err) for err in e.error_log])
        return False, f"XML Validation Error: {errors}"
    except Exception as e:
        return False, f"Unexpected validation error: {e}"
    
    
def save_results_to_csv(successful_urls, failed_urls, script_dir):
    """Saves successful and failed URLs to a CSV file."""
    file_path = os.path.join(script_dir, 'scraping_results.csv')
    try:
        with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Updated header to include 'Failed XML Content'
            writer.writerow(['URL', 'Status', 'Error', 'Failed XML Content'])
            for url in successful_urls:
                writer.writerow([url, 'Success', '', ''])
            for url, error, failed_xml_content in failed_urls:
                # Replace newlines in XML content for CSV compatibility
                xml_to_write = failed_xml_content.replace('\n', ' ').strip() if failed_xml_content else ''
                writer.writerow([url, 'Failed', str(error).replace('\n', ' ').strip(), xml_to_write])
        print(f"\nResults saved to {file_path}")
    except IOError as e:
        print(f"\nError saving results to CSV: {e}")


def insert_into_database(xml_file_path):
    insert_recipe_from_xml(xml_file_path)

# Changed to synchronous function
def fetch_and_process_url(url):
    """
    Synchronously fetches a URL, then processes its content.
    """
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        html = response.text
        # Parsing and XML creation are CPU-bound and done synchronously
        recipe_data = parse_recipe_content(html, url)
        if recipe_data:
            xml_output = create_xml(recipe_data)
            return url, xml_output, None # url, data, error
        else:
            return url, None, "Failed to parse recipe data."
    except Exception as e:
        return url, None, str(e)

# Changed to synchronous function
def main():
    sitemap_urls = [
        "https://pinchofyum.com/post-sitemap.xml",
        "https://pinchofyum.com/post-sitemap2.xml",
    ]
    
    successful_urls = []
    # Modified failed_urls to store (url, error, xml_content)
    failed_urls = []
    
    print("--- Starting Sitemap Scraping ---")
    all_urls = []
    for sitemap_url in sitemap_urls:
        all_urls.extend(scrape_sitemap_urls(sitemap_url))

    urls = sorted(list(set(all_urls)))
    total_urls = len(urls)
    
    if urls:
        print("-" * 50)
        print(f"Found a total of {total_urls} unique URLs to process.")
        
        script_dir = os.path.dirname(os.path.realpath(__file__))
        rng_path = os.path.join(script_dir, 'recipe_schema.rng')
        xml_path = os.path.join(script_dir, 'recipe.xml') # Single XML file

        if not os.path.exists(rng_path):
            print(f"XSD file not found at {rng_path}. Please create it before running.")
            return

        processed_count = 0
        # Replaced async processing with synchronous loop
        for url in urls:
            scraped_url, xml_output, error_msg = fetch_and_process_url(url)
            
            processed_count += 1
            progress = processed_count / total_urls
            sys.stdout.write(f"\rProcessing: [{int(progress * 20) * '='}>{(20 - int(progress * 20)) * ' '}] {int(progress * 100)}% ({processed_count}/{total_urls})")
            sys.stdout.flush()

            # First, check if we have valid XML output. If not, log the failure and skip.
            if not xml_output:
                error_to_log = error_msg or "Unknown error: XML output was None."
                # Append None for XML content if it's not generated
                failed_urls.append((scraped_url, error_to_log, None)) 
                continue

            # Now that we know xml_output is a string, we can write it.
            with open(xml_path, 'w', encoding='utf-8') as f:
                f.write(xml_output)

            is_valid, validation_error = validate_xml(xml_path, rng_path)
            if is_valid:
                successful_urls.append(scraped_url)
                insert_into_database(xml_path)
            else:
                # Append the generated xml_output when validation fails
                failed_urls.append((scraped_url, validation_error, xml_output))
        
        print(f"\n\n--- SCRAPING AND VALIDATION COMPLETE ---")
        print(f"✅ Successfully validated: {len(successful_urls)}")
        print(f"❌ Failed validation: {len(failed_urls)}")

        if failed_urls:
            # Optionally print failures here if desired
            pass
        
        save_choice = input("\nDo you want to save the results to a CSV file? (y/n): ").lower()
        if save_choice == 'y':
            save_results_to_csv(successful_urls, failed_urls, script_dir)
    else:
        print("No URLs were extracted from the sitemaps.")

if __name__ == "__main__":
    # Removed async-related setup and call
    main()