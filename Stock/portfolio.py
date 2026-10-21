import csv
import os

# Project directory
ROOT_DIR = r"D:\26r15a0538\Task\Stock"

# File paths
DATASET_FILE = os.path.join(ROOT_DIR, "constituents.csv")
PORTFOLIO_FILE = os.path.join(ROOT_DIR, "portfolio.csv")
SUMMARY_FILE = os.path.join(ROOT_DIR, "portfolio_summary.csv")


def load_stocks():
    """Load company names and ticker symbols from the provided dataset."""

    stocks = {}

    try:
        with open(DATASET_FILE, "r", newline="", encoding="utf-8-sig") as file:
            reader = csv.DictReader(file)

            for row in reader:
                ticker = row["Symbol"].strip().upper()
                company = row["Security"].strip()

                if ticker and company:
                    stocks[ticker] = company

    except FileNotFoundError:
        print("Error: constituents.csv was not found.")
        print("Place the dataset inside:", ROOT_DIR)
        return {}

    except (KeyError, csv.Error) as error:
        print("Error reading the dataset:", error)
        return {}

    return stocks


def get_positive_number(message):
    """Accept only positive numeric values."""

    while True:
        try:
            value = float(input(message))

            if value > 0:
                return value

            print("Enter a value greater than zero.")

        except ValueError:
            print("Invalid input. Enter a number.")


def load_portfolio():
    """Load previously saved portfolio holdings."""

    holdings = {}

    if not os.path.exists(PORTFOLIO_FILE):
        return holdings

    try:
        with open(
            PORTFOLIO_FILE, "r", newline="", encoding="utf-8"
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                ticker = row["Ticker"]

                holdings[ticker] = {
                    "company": row["Company"],
                    "quantity": int(row["Quantity"]),
                    "purchase_price": float(row["Purchase Price"]),
                    "current_price": float(row["Current Price"])
                }

    except (OSError, ValueError, KeyError, csv.Error) as error:
        print("Could not load saved portfolio:", error)

    return holdings


def save_portfolio(holdings):
    """Save portfolio holdings to a CSV file."""

    with open(
        PORTFOLIO_FILE, "w", newline="", encoding="utf-8"
    ) as file:
        fieldnames = [
            "Ticker",
            "Company",
            "Quantity",
            "Purchase Price",
            "Current Price"
        ]

        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for ticker, stock in holdings.items():
            writer.writerow({
                "Ticker": ticker,
                "Company": stock["company"],
                "Quantity": stock["quantity"],
                "Purchase Price": stock["purchase_price"],
                "Current Price": stock["current_price"]
            })


def add_stock(stocks, holdings):
    """Add a stock from the provided S&P 500 dataset."""

    ticker = input("Enter stock ticker: ").strip().upper()

    if ticker not in stocks:
        print("Ticker not found in the provided S&P 500 dataset.")
        return

    company = stocks[ticker]

    print("\nCompany:", company)

    quantity = get_positive_number("Enter quantity of shares: ")
    purchase_price = get_positive_number("Enter purchase price per share: $")
    current_price = get_positive_number("Enter current price per share: $")

    if not quantity.is_integer():
        print("Quantity must be a whole number.")
        return

    holdings[ticker] = {
        "company": company,
        "quantity": int(quantity),
        "purchase_price": purchase_price,
        "current_price": current_price
    }

    save_portfolio(holdings)

    print(f"\n{company} added to your portfolio successfully.")


def view_portfolio(holdings):
    """Display holdings and calculate portfolio performance."""

    if not holdings:
        print("\nYour portfolio is empty.")
        return

    total_investment = 0
    total_value = 0

    print("\n" + "=" * 100)
    print("PORTFOLIO PERFORMANCE")
    print("=" * 100)

    print(
        f"{'Ticker':<10}"
        f"{'Company':<28}"
        f"{'Qty':>6}"
        f"{'Buy Price':>14}"
        f"{'Current':>14}"
        f"{'Profit/Loss':>14}"
        f"{'Return %':>12}"
    )

    print("-" * 100)

    for ticker, stock in holdings.items():
        quantity = stock["quantity"]
        purchase_price = stock["purchase_price"]
        current_price = stock["current_price"]

        investment = quantity * purchase_price
        value = quantity * current_price
        profit_loss = value - investment
        return_percent = (profit_loss / investment) * 100

        total_investment += investment
        total_value += value

        print(
            f"{ticker:<10}"
            f"{stock['company'][:26]:<28}"
            f"{quantity:>6}"
            f"${purchase_price:>13,.2f}"
            f"${current_price:>13,.2f}"
            f"${profit_loss:>13,.2f}"
            f"{return_percent:>11.2f}%"
        )

    total_profit_loss = total_value - total_investment

    if total_investment:
        total_return = (total_profit_loss / total_investment) * 100
    else:
        total_return = 0

    print("-" * 100)
    print(f"Total Investment : ${total_investment:,.2f}")
    print(f"Current Value    : ${total_value:,.2f}")
    print(f"Total Profit/Loss: ${total_profit_loss:,.2f}")
    print(f"Overall Return   : {total_return:.2f}%")
    print("=" * 100)


def export_summary(holdings):
    """Export calculated portfolio performance to a CSV file."""

    if not holdings:
        print("\nYour portfolio is empty. Nothing to export.")
        return

    fieldnames = [
        "Ticker",
        "Company",
        "Quantity",
        "Purchase Price",
        "Current Price",
        "Total Investment",
        "Current Value",
        "Profit/Loss",
        "Return Percentage"
    ]

    with open(
        SUMMARY_FILE, "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for ticker, stock in holdings.items():
            quantity = stock["quantity"]
            purchase_price = stock["purchase_price"]
            current_price = stock["current_price"]

            investment = quantity * purchase_price
            value = quantity * current_price
            profit_loss = value - investment
            return_percent = (profit_loss / investment) * 100

            writer.writerow({
                "Ticker": ticker,
                "Company": stock["company"],
                "Quantity": quantity,
                "Purchase Price": f"{purchase_price:.2f}",
                "Current Price": f"{current_price:.2f}",
                "Total Investment": f"{investment:.2f}",
                "Current Value": f"{value:.2f}",
                "Profit/Loss": f"{profit_loss:.2f}",
                "Return Percentage": f"{return_percent:.2f}"
            })

    print("\nPortfolio summary exported to:")
    print(SUMMARY_FILE)


def main():
    """Run the portfolio tracker."""

    print("=" * 50)
    print(" STOCK PORTFOLIO PERFORMANCE TRACKER")
    print("=" * 50)

    stocks = load_stocks()

    if not stocks:
        print("\nUnable to load the stock dataset.")
        print("Check that constituents.csv is in the project folder.")
        return

    holdings = load_portfolio()

    print(f"\nLoaded {len(stocks)} companies from the dataset.")
    print(f"Loaded {len(holdings)} saved portfolio holdings.")

    while True:
        print("\nMENU")
        print("1. Search for a stock")
        print("2. Add or update a stock holding")
        print("3. View portfolio performance")
        print("4. Export portfolio summary")
        print("5. Exit")

        choice = input("\nChoose an option (1-5): ").strip()

        if choice == "1":
            query = input(
                "Enter a company name or ticker: "
            ).strip().lower()

            matches = [
                (ticker, company)
                for ticker, company in stocks.items()
                if query in ticker.lower()
                or query in company.lower()
            ]

            if matches:
                print("\nMatching stocks:")

                for ticker, company in matches[:20]:
                    print(f"{ticker:<10} {company}")

                if len(matches) > 20:
                    print("Showing the first 20 matches.")
            else:
                print("No matching stocks found.")

        elif choice == "2":
            add_stock(stocks, holdings)

        elif choice == "3":
            view_portfolio(holdings)

        elif choice == "4":
            export_summary(holdings)

        elif choice == "5":
            print("Portfolio tracker closed.")
            break

        else:
            print("Invalid choice. Select an option from 1 to 5.")


if __name__ == "__main__":
    main()