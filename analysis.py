import pandas as pd

# df=pd.read_csv("api_data_aadhar_demographic_0_500000.csv")
# print(df.head())
# print(df["state_name"].unique())

files=["api_data_aadhar_demographic_0_500000.csv",
       "api_data_aadhar_demographic_500000_1000000.csv",
       "api_data_aadhar_demographic_1000000_1500000.csv",
       "api_data_aadhar_demographic_1500000_2000000.csv",
       "api_data_aadhar_demographic_2000000_2071700.csv"]

df=pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
print("Total Records:", len(df))

print("Unique Raw States:", df['state'].nunique())
print(df['state'].unique())

df["state_clean"]=df["state"].str.lower().str.strip()
print(sorted(df["state_clean"].unique()))

fix_map={
    "orissa": "odisha",
    "pondicherry": "puducherry",

    "west bangal": "west bengal",
    "westbengal": "west bengal",
    "west  bengal": "west bengal",
    "west bengli": "west bengal", 

    "jammu & kashmir": "jammu and kashmir",

    "andaman & nicobar islands": "andaman and nicobar islands",
    "jaipur": "rajasthan",
    "nagpur": "maharashtra",
    "uttaranchal": "uttarakhand",

    "chhatisgarh": "chhattisgarh",
    "darbhanga": "bihar",
    "madanapalle": "andhra pradesh",
    "puttenahalli": "karnataka",
    "raja annamalai puram": "tamil nadu",

    "dadra & nagar haveli": "dadra and nagar haveli and daman and diu",
    "daman and diu": "dadra and nagar haveli and daman and diu",
    "daman & diu": "dadra and nagar haveli and daman and diu",
    "dadra and nagar haveli": "dadra and nagar haveli and daman and diu",
    "balanagar": "telangana",
    "100000": None
}
df["state_clean"]=df["state_clean"].replace(fix_map)
df=df[ df["state_clean"].notna()]

print("\nSTEP2.4 Final Clean Result:")
print("Final Clean States and UTs", df['state_clean'].nunique())
print(sorted(df['state_clean'].unique()))  


df["total_enrolled"]=df["demo_age_5_17"]+df["demo_age_17_"] 

state_summary=(
    df.groupby("state_clean")["total_enrolled"]
    .sum()
    .reset_index() 
    .sort_values(by="total_enrolled", ascending=False)
)
print(state_summary)  

print("\nTop 10 States/UTs by Aadhar Enrollments:")
print(state_summary.head(10)) 

print("\nBottom 10 States/UTs by Aadhar Enrollments:")
print(state_summary.tail(10))


state_summary = state_summary.reset_index(drop=True)
state_summary["Overall_Rank"] = range(1, len(state_summary) + 1)

top10=state_summary.head(10).copy()
top10=top10.reset_index(drop=True)
top10["Top10_Rank"]=range(1, len(top10)+1)

print("\n⭐️ Top 10 States/UTs (CLEAN RANKING 1-10):")
print(
    top10[["Top10_Rank", "state_clean", "total_enrolled"]]
    .to_string(index=False) 
)


bottom10=state_summary.tail(10).copy()
bottom10=bottom10.reset_index(drop=True)
bottom10["Bottom10_Rank"]=range(1, len(bottom10)+1)

print("\n⚠️ Bottom 10 States/UTs (CLEAN RANKING 1-10):")
print(
    bottom10[["Bottom10_Rank", "state_clean", "total_enrolled"]]
    .to_string(index=False) 
)

import matplotlib.pyplot as plt
colors = ["#ce4040", "#6643e4", "#7bdf72"]

plt.figure(figsize=(10,5))
bars = plt.bar(
    top10["state_clean"],
    top10["total_enrolled"],
    color=colors * 4   # repeat colors automatically
)

plt.xticks(rotation=45, ha="right")
plt.title("Top 10 States by Aadhaar Enrolment")
plt.xlabel("States/UTs")
plt.ylabel("Total New Aadhaar Enrolments")
plt.ticklabel_format(style="plain", axis="y")

for bar in bars:
    h = bar.get_height()
    plt.text(bar.get_x()+bar.get_width()/2, h, f"{int(h):,}",
             ha="center", va="bottom", fontsize=9)

plt.tight_layout()


plt.figure(figsize=(10,5))
bars = plt.bar(
    bottom10["state_clean"],
    bottom10["total_enrolled"],
    color=colors * 4
)

plt.xticks(rotation=45, ha="right")
plt.title("Bottom 10 States by Aadhaar Enrolment")
plt.xlabel("State")
plt.ylabel("Total New Aadhaar Enrolments")
plt.ticklabel_format(style="plain", axis="y")

for bar in bars:
    h = bar.get_height()
    plt.text(bar.get_x()+bar.get_width()/2, h, f"{int(h):,}",
             ha="center", va="bottom", fontsize=9)

plt.tight_layout()

df["date"] = pd.to_datetime(
    df["date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)

df = df[df["date"].notna()]

daily_pulse = (
    df.groupby("date")["total_enrolled"]
      .sum()
      .reset_index()
)


plt.figure(figsize=(12,5))
plt.plot(
    daily_pulse["date"],
    daily_pulse["total_enrolled"],
    color=colors[1],   # pick any one
    marker="o",
    linewidth=2
)

plt.title("Aadhaar Enrolment Pulse Over Time")
plt.xlabel("Date")
plt.ylabel("Total New Aadhaar Enrolments")
plt.ticklabel_format(style="plain", axis="y")
plt.xticks(rotation=45)
plt.grid(True)

plt.tight_layout()


plt.figure(figsize=(6,6))
plt.pie(
    [
        df["demo_age_5_17"].sum(),
        df["demo_age_17_"].sum()
    ],
    labels=["Age 5-17", "Age 17 and above"],
    autopct=lambda p: f"{p:.1f}%",
    startangle=90,
    colors=colors
)

plt.title("Aadhaar Enrolments by Age Group")
plt.tight_layout()
plt.show()