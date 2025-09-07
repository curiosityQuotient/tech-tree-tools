import pandas as pd

fp = "freeciv_raw.csv"

tech_df = pd.read_csv(fp)
tech_df = tech_df.fillna("None")

tech_df["Type"] = "requirement"

tech_filter = tech_df["Description"].str.contains("Total tech")
tech_df.loc[tech_filter, "Type"] = "dependent"

df_copy = tech_df.copy().reset_index(drop=True)

# Find which A each row belongs to by forward-filling A indices
a_indices = df_copy[df_copy["Type"] == "dependent"].index
df_copy["a_group"] = None

current_a_idx = None
for idx in df_copy.index:
    if df_copy.loc[idx, "Type"] == "dependent":
        current_a_idx = idx
    df_copy.loc[idx, "a_group"] = current_a_idx

# Group B strings by their corresponding A
b_strings_by_a = {}
for idx, row in df_copy.iterrows():
    if row["Type"] == "requirement" and row["a_group"] is not None:
        a_idx = row["a_group"]
        if a_idx not in b_strings_by_a:
            b_strings_by_a[a_idx] = []
        b_strings_by_a[a_idx].append(row["Tech requirements"])

# Create result with only A rows
result = df_copy[df_copy["Type"] == "dependent"].copy()

# Add B strings as lists (or join them as single strings)
result["b_strings_list"] = result.index.map(lambda x: b_strings_by_a.get(x, []))

# Also create a joined version
result["b_strings_joined"] = result["b_strings_list"].apply(
    lambda x: "".join(x) if x else ""
)

result["b_strings_joined"] = result["b_strings_joined"].str.replace(",", ";")

output_df = result.loc[:, ["Tech requirements", "b_strings_joined"]]
output_df = output_df.rename(
    columns={"Tech requirements": "Name", "b_strings_joined": "Predecessors"}
)
output_df["Successors"] = ""

output_df.to_csv("freeciv_tech_tree.csv", index=False)

print("x")

# Note: Lvl 1 tech costs 28 bulbs, lvl 2 costs 79-28 = 51
bulb_func = lambda x: ((x + 2)*(x + 2)**0.5)*10 // 1