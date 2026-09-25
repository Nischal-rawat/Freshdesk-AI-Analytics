import pandas as pd


class DatasetValidator:

    def __init__(self, df):
        self.df = df

    def validate(self):

        print("\n" + "=" * 70)
        print("DATASET VALIDATION REPORT")
        print("=" * 70)

        print(f"Rows                 : {len(self.df):,}")
        print(f"Columns              : {len(self.df.columns)}")
        print(f"Duplicate Rows       : {self.df.duplicated().sum()}")

        empty_columns = [
            c for c in self.df.columns
            if self.df[c].isna().all()
        ]

        unnamed_columns = [
            c for c in self.df.columns
            if str(c).startswith("Unnamed")
        ]

        print(f"Empty Columns        : {len(empty_columns)}")
        print(f"Unnamed Columns      : {len(unnamed_columns)}")

        print("\nCOLUMN PROFILE")
        print("-" * 70)

        profile = []

        for column in self.df.columns:

            dtype = str(self.df[column].dtype)

            missing = self.df[column].isna().sum()

            missing_pct = round(
                missing / len(self.df) * 100,
                2
            )

            unique = self.df[column].nunique(dropna=True)

            recommendation = "Keep"

            if str(column).startswith("Unnamed"):
                recommendation = "Remove"

            elif missing_pct == 100:
                recommendation = "Remove"

            elif unique <= 1:
                recommendation = "Review"

            profile.append([
                column,
                dtype,
                missing_pct,
                unique,
                recommendation
            ])

        profile_df = pd.DataFrame(
            profile,
            columns=[
                "Column",
                "Data Type",
                "% Missing",
                "Unique Values",
                "Recommendation"
            ]
        )

        print(profile_df)

        print("\n" + "=" * 70)

        return profile_df