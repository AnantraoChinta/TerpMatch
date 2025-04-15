import scraper
import csv_convert

# Defining main function
def main():
    json_file = scraper.scrape_clubs()
    csv_file = "clubs.csv"
    csv_convert.json_to_csv(json_file, csv_file)


if __name__=="__main__":
    main()