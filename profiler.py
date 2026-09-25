import pandas as pd


class DatasetProfiler:

    def __init__(self, df):
        self.df = df

    def profile(self):

        print("\n" + "=" * 70)
        print("DATASET PROFILE")
        print("=" * 70)

        print(f"Rows                : {len(self.df):,}")
        print(f"Columns             : {len(self.df.columns)}")

        # Show important fields if they exist
        important_columns = [
            "Ticket ID",
            "Requester",
            "Status",
            "Priority",
            "Group",
            "Agent",
            "Created Time",
            "Resolved Time",
            "Resolution Time"
        ]

        print("\nAVAILABLE IMPORTANT COLUMNS")
        print("-" * 70)

        for col in important_columns:
            if col in self.df.columns:
                print(f"✓ {col}")

        print("\nCOLUMN DATA TYPES")
        print("-" * 70)

        print(self.df.dtypes.value_counts())

        print("\nTOP 20 COLUMNS WITH LEAST MISSING DATA")
        print("-" * 70)

        completeness = (
            100 - (self.df.isna().mean() * 100)
        ).sort_values(ascending=False)

        print(completeness.head(20))

        print("\nTOP 20 COLUMNS WITH MOST MISSING DATA")
        print("-" * 70)

        print(completeness.tail(20))

        print("\n" + "=" * 70)