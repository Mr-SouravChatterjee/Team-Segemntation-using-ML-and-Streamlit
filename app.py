import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import base64
from PIL import Image
import os

def load_logo_as_base64(file_path):
    with open(file_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

logo_base64 = load_logo_as_base64("pictures/logo.png")
st.set_page_config(page_title="VTS Enterprises", page_icon=f"data:image/png;base64,{logo_base64}")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def load_csv(file_name):
    if os.path.exists(file_name):
        return pd.read_csv(file_name)
    else:
        return pd.DataFrame(columns=["Task Name", "Team Number", "Deadline", "Status"])

def save_csv(df, file_name):
    df.to_csv(file_name, index=False)

tasks_file = "tasks.csv"
tasks_df = load_csv(tasks_file)

# Plotting Functions (As defined before)

# Data Cleaning Functions (As defined before)

# Team Segmentation Functions (As defined before)

# Task Monitoring Functions
def task_monitoring_page():
    st.image("pictures/full logo.png", use_column_width=True)
    st.title("Task Monitoring Tool")
    st.markdown("""
Welcome to the **Task Monitoring Tool**, developed by **Team Zigma** to streamline your project management process. This tool allows you to efficiently track and monitor tasks assigned to various teams, ensuring timely completion and smooth workflow.

---

### Key Features:
- **Assign Tasks**: Easily assign new tasks to specific teams, set deadlines, and track their status.
- **Monitor Progress**: View and update the status of ongoing tasks, helping you keep track of progress and ensure deadlines are met.
- **Track Deadlines**: Stay on top of deadlines with clear visibility into upcoming and overdue tasks.

---
""")

    # Assign New Task
    st.subheader("Assign New Task")
    task_name = st.text_input("Task Name")
    team_number = st.text_input("Enter Team Number") 
    deadline = st.date_input("Select Deadline")
    status = st.selectbox("Select Status", ["Not Started", "In Progress", "Completed"])

    if st.button("Assign Task"):
        if task_name:
            new_task = pd.DataFrame({
                "Task Name": [task_name],
                "Team Number": [team_number],
                "Deadline": [deadline],
                "Status": [status]
            })
            global tasks_df
            tasks_df = pd.concat([tasks_df, new_task], ignore_index=True)
            save_csv(tasks_df, tasks_file)
            st.success(f"Task '{task_name}' assigned to {team_number} with a deadline of {deadline} and status '{status}'.")

    # Remove Task
    st.subheader("Remove Task")
    remove_task_name = st.selectbox("Select Task to Remove", tasks_df["Task Name"].unique())
    if st.button("Remove Task"):
        tasks_df = tasks_df[tasks_df["Task Name"] != remove_task_name]
        save_csv(tasks_df, tasks_file)
        st.success(f"Task '{remove_task_name}' removed successfully.")

    # Update Task
    st.subheader("Update Task")
    update_task_name = st.selectbox("Select Task to Update", tasks_df["Task Name"].unique())
    new_status = st.selectbox("New Status", ["Not Started", "In Progress", "Completed"])
    if st.button("Update Task"):
        tasks_df.loc[tasks_df["Task Name"] == update_task_name, "Status"] = new_status
        save_csv(tasks_df, tasks_file)
        st.success(f"Task '{update_task_name}' status updated to '{new_status}'.")

    # Track Tasks
    st.subheader("Track Tasks")
    if not tasks_df.empty:
        st.write("### Task List")
        st.dataframe(tasks_df)
    else:
        st.write("No tasks assigned yet.")
        
# Plotting Functions
def plot_job_role_distribution(df):
    plt.figure(figsize=(7, 5))
    sns.countplot(y='Job Role', data=df, palette='pastel', order=df['Job Role'].value_counts().index, hue='Job Role', dodge=False)
    plt.title('Job Role Distribution')
    plt.xlabel('Number of Employees')
    plt.ylabel('Job Role')
    st.pyplot(plt.gcf())
    plt.close()

def plot_performance_rating_distribution(df):
    plt.figure(figsize=(7, 5))
    sns.countplot(x='Performance Rating', data=df, palette='pastel', hue='Performance Rating', dodge=False)
    plt.title('Distribution of Performance Ratings')
    plt.xlabel('Performance Rating')
    plt.ylabel('Number of Employees')
    st.pyplot(plt.gcf())
    plt.close()

def plot_job_roles_vs_performance(df):
    top_job_roles = df['Job Role'].value_counts().nlargest(5).index
    filtered_df = df[df['Job Role'].isin(top_job_roles)]
    plt.figure(figsize=(8, 6), facecolor='white')
    sns.countplot(x='Job Role', hue='Performance Rating', data=filtered_df, palette=['lightgreen', 'pink'])
    plt.title('Job Roles vs. Performance Rating')
    plt.xlabel('Job Role')
    plt.ylabel('Count of Employees')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.close()

def plot_top_job_roles_by_performance(df):
    plt.figure(figsize=(7, 5))
    avg_performance_by_role = df.groupby('Job Role')['Performance Rating'].mean().sort_values(ascending=False)
    sns.barplot(x=avg_performance_by_role.values, y=avg_performance_by_role.index, palette='pastel', hue=avg_performance_by_role.index, dodge=False)
    plt.title('Top Job Roles by Average Performance Rating')
    plt.xlabel('Average Performance Rating')
    plt.ylabel('Job Role')
    st.pyplot(plt.gcf())
    plt.close()

def plot_gender_distribution(df):
    plt.figure(figsize=(7, 5))
    gender_counts = df['Gender'].value_counts()
    plt.pie(gender_counts, labels=gender_counts.index, autopct='%1.1f%%', colors=sns.color_palette('pastel'))
    plt.title('Gender Distribution')
    st.pyplot(plt.gcf())
    plt.close()

def plot_gender_distribution_in_job_roles(df):
    plt.figure(figsize=(7, 5))
    sns.countplot(y='Job Role', hue='Gender', data=df, palette='pastel')
    plt.title('Gender Distribution Across Job Roles')
    plt.xlabel('Number of Employees')
    plt.ylabel('Job Role')
    st.pyplot(plt.gcf())
    plt.close()

def plot_gender_vs_performance_rating(df):
    plt.figure(figsize=(7, 5))
    sns.countplot(x='Gender', hue='Performance Rating', data=df, palette=['pink', 'violet'])
    plt.title('Gender vs. Performance Rating')
    plt.xlabel('Gender')
    plt.ylabel('Count of Employees')
    plt.tight_layout()
    st.pyplot(plt.gcf())
    plt.close()

def plot_experience_distribution(df):
    plt.figure(figsize=(7, 5))
    sns.histplot(df['Experience'], kde=False, color='skyblue', bins=10)
    plt.title('Distribution of Experience')
    plt.xlabel('Years of Experience')
    plt.ylabel('Number of Employees')
    st.pyplot(plt.gcf())
    plt.close()

def plot_experience_vs_performance_rating(df):
    plt.figure(figsize=(7, 5))
    sns.boxplot(x='Performance Rating', y='Experience', data=df, palette='coolwarm', hue='Performance Rating', dodge=False)
    plt.title('Experience vs. Performance Rating')
    plt.xlabel('Performance Rating')
    plt.ylabel('Years of Experience')
    st.pyplot(plt.gcf())
    plt.close()

def plot_performance_rating_by_yoe():
    experience_years = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    performance_rating_3 = [5, 10, 15, 20, 25, 30, 20, 10, 5, 3, 2]
    performance_rating_5 = [0, 2, 5, 10, 15, 20, 30, 25, 20, 15, 10]

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    axes[0].bar(experience_years, performance_rating_3, color='lightcoral', alpha=0.7)
    axes[0].set_xticks(experience_years)
    axes[0].set_title("Distribution of Performance (PR-3) by YOE")
    axes[0].set_xlabel("Years of Experience")
    axes[0].set_ylabel("Counts")
    axes[0].grid(axis='y')

    axes[1].bar(experience_years, performance_rating_5, color='lightblue', alpha=0.7)
    axes[1].set_xticks(experience_years)
    axes[1].set_title("Distribution of Performance (PR-5) by YOE")
    axes[1].set_xlabel("Years of Experience")
    axes[1].set_ylabel("Counts")
    axes[1].grid(axis='y')

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

def plot_top_skills(df):
    plt.figure(figsize=(7, 5))
    skills = df['Skills'].str.get_dummies(sep=' ').sum().sort_values(ascending=False).head(10)
    sns.barplot(x=skills.values, y=skills.index, palette='pastel', hue=skills.index, dodge=False)
    plt.title('Top 10 Skill Distribution Among Employees')
    plt.xlabel('Number of Employees with Skill')
    plt.ylabel('Skills')
    st.pyplot(plt.gcf())
    plt.close()


# Data Loading and Cleaning Functions
def load_csv():
    uploaded_file = st.file_uploader("📁 Upload your CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data
    else:
        st.warning("Please upload a CSV file.")
        return None



def clean_data(data):
    data = data.drop_duplicates()
    data['Employee ID'] = data.index  # Preserve original index
    data = data.fillna({
        'Name': 'Unknown',
        'Experience': 0,
        'Job Role': 'Unknown',
        'Gender': 'Unknown',
        'Skills': '',
        'Phone Number': 'Unknown',
        'Email': 'Unknown',
        'Employment Status': 'Unknown',
        'Preferences': 'None'
    })
    data['Experience'] = pd.to_numeric(data['Experience'], errors='coerce').fillna(0)
    return data

def load_excel():
    uploaded_file = st.file_uploader("📁 Upload your CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        return data
    else:
        st.warning("Please upload a CSV file.")
        return None

# Team Segmentation Functions
def get_input():
    st.sidebar.header("Team Formation Parameters")
    num_teams = st.sidebar.number_input("Number of Teams:", min_value=1, value=1)
    team_size = st.sidebar.number_input("Members per Team(min):", min_value=1, value=1)
    required_skills = st.sidebar.text_input("Required Skills (comma-separated):").split(',')
    required_skills = [skill.strip() for skill in required_skills if skill.strip()]
    return num_teams, team_size, required_skills

def filter_candidates(data, required_skills):
    if required_skills:
        filtered_data = data[data['Skills'].str.contains('|'.join(required_skills), case=False, na=False)]
    else:
        filtered_data = data
    return filtered_data

def form_balanced_teams(filtered_data, num_teams, team_size, required_skills):
    teams = [[] for _ in range(num_teams)]
    skill_candidates = {skill: [] for skill in required_skills}
    
    for skill in required_skills:
        skill_candidates[skill] = filtered_data[filtered_data['Skills'].str.contains(skill, case=False, na=False)].to_dict('records')
    
    all_candidates = []
    for skill in required_skills:
        all_candidates.extend(skill_candidates[skill])
    
    import random
    random.shuffle(all_candidates)
    
    team_idx = 0
    for candidate in all_candidates:
        if len(teams[team_idx]) < team_size:
            teams[team_idx].append(candidate)
        else:
            team_idx = (team_idx + 1) % num_teams
            teams[team_idx].append(candidate)
    
    teams = [pd.DataFrame(team) for team in teams]
    
    warnings = []
    for skill in required_skills:
        if len(skill_candidates[skill]) == 0:
            warnings.append(f"No candidates with the skill {skill} available in the dataset.")
    
    return teams, warnings

def display_teams(teams, warnings):
    for i, team in enumerate(teams):
        st.subheader(f"🎯 Team {i+1}:")
        if not team.empty:
            # Display 'Original Index' along with other columns
            st.dataframe(team[['Employee ID', 'Name', 'Experience', 'Job Role', 'Skills']].set_index('Employee ID'))
        else:
            st.write("No members in this team.")
    if warnings:
        st.subheader("⚠️ Warnings")
        for warning in warnings:
            st.write(warning)


# Navigation Functions
def main_page():
    st.image("pictures/full logo.png", use_column_width=True)
    st.title("VTS Project Dashboard")
    st.markdown("""
Welcome to the VTS Project Dashboard, proudly developed by **Team Zigma**. This platform is your one-stop solution for seamless team management and insightful data analysis, designed to optimize performance and decision-making.

---

### About Team Zigma
At **Team Zigma**, we believe in delivering excellence through innovation. Our team segmentation tool is crafted to help you effortlessly organize teams based on specific skills and requirements, ensuring that every project has the right mix of talent.

---

### Explore the Dashboard
- **Team Segmentation Tool**: Efficiently segment your team members based on various criteria such as skills, experience, and job roles. This tool is designed to streamline the process of team formation, ensuring balanced and effective teams.

- **Data Analysis**: Dive into comprehensive data analysis with our dashboard. Visualize key metrics like job role distribution, performance ratings, skills, and more to gain valuable insights that drive strategic decisions.

- **Task Monitoring Tool**: Keep track of assigned tasks, deadlines, and their status. This tool helps you manage and monitor ongoing tasks efficiently, ensuring timely completion and effective task allocation.

- **Contact Us**: Have any questions or need support? Visit our Contact Us page to reach out, and we'll be happy to assist you.

---

### Getting Started
Navigate through the dashboard using the sidebar to access the tools and features that best suit your needs. Whether you're forming teams, analyzing data, or tracking tasks, our platform is designed to make your experience smooth and intuitive.

---

Thank you for choosing **Team Zigma** and the **VTS Project Dashboard**. Let's achieve great things together!
""")


def team_segmentation_page():
    st.image("pictures/full logo.png", use_column_width=True)
    st.title("Team Segmentation Tool")
    local_css("styles.css")
    st.markdown("Welcome to the **Team Segmentation Tool**, a smart solution designed by **Team Zigma** to help you build balanced and effective teams based on specific criteria. Upload your dataset, set your team parameters, and let the tool automatically form teams based on your requirements.")
    st.markdown("---")
    data = load_csv()
    if data is not None:
        st.subheader("🔍 Full Data Preview")
        st.dataframe(data)
        data = clean_data(data)
        st.subheader("✨ Full Cleaned Data Preview")
        st.dataframe(data)
        num_teams, team_size, required_skills = get_input()
        if st.sidebar.button("Form Teams"):
            filtered_data = filter_candidates(data, required_skills)
            teams, warnings = form_balanced_teams(filtered_data, num_teams, team_size, required_skills)
            display_teams(teams, warnings)


def data_analysis_page():
    st.image("pictures/full logo.png", use_column_width=True)
    st.title("Employee Data Analysis")
    df = load_excel()
    
    st.sidebar.title("Visualizations")
    visualization = st.sidebar.radio("Select a visualization:", 
                                     ["Home",  
                                      "Job Role Distribution", 
                                      "Performance Rating Distribution", 
                                      "Job Roles vs. Performance Rating", 
                                      "Top Job Roles by Performance Rating", 
                                      "Gender Distribution", 
                                      "Gender Distribution in Job Roles", 
                                      "Gender vs. Performance Rating", 
                                      "Experience Distribution", 
                                      "Experience vs. Performance Rating", 
                                      "Performance Rating by Years of Experience", 
                                      "Top 10 Skills"])

    if visualization == "Home":
        st.subheader("Employee Data Analysis Dashboard")
        st.write("""
        Welcome to the EDA dashboard which is designed to provide a comprehensive analysis of employee data,
        focusing on performance ratings, job roles, skills, gender distribution, and more.
        
        Use the sidebar to navigate through various visualizations and gain insights into the
        employee dataset. The visualizations help to identify key trends and patterns that 
        can inform decision-making and strategic planning.
        """)
        st.markdown(
        """
        <div style="display: flex; justify-content: center; align-items: center;">
            <video width="800" height="400" controls>
                <source src="https://videos.pexels.com/video-files/6774467/6774467-uhd_1440_2560_30fps.mp4" type="video/mp4">
                Your browser does not support the video tag.
            </video>
        </div>
        <p style="text-align: center; font-size: 18px; margin-top: 10px;">Brought to you by: Team Zigma</p>
        """,
        unsafe_allow_html=True
        )
        st.markdown("### Key Features:")
        st.markdown("""    
    - **Job Role Distribution**: Understand the spread of job roles across the company.
    - **Performance Ratings**: Analyze performance ratings by various factors such as job roles and experience.
    - **Skills Analysis**: Explore the top skills among employees.
    - **Gender Distribution**: Review gender distribution in different job roles and performance ratings.
    - **Experience Analysis**: Examine how experience impacts performance.
    """)
        
    if visualization == "Job Role Distribution":
        plot_job_role_distribution(df)
    elif visualization == "Performance Rating Distribution":
        plot_performance_rating_distribution(df)
    elif visualization == "Job Roles vs. Performance Rating":
        plot_job_roles_vs_performance(df)
    elif visualization == "Top Job Roles by Performance Rating":
        plot_top_job_roles_by_performance(df)
    elif visualization == "Gender Distribution":
        plot_gender_distribution(df)
    elif visualization == "Gender Distribution in Job Roles":
        plot_gender_distribution_in_job_roles(df)
    elif visualization == "Gender vs. Performance Rating":
        plot_gender_vs_performance_rating(df)
    elif visualization == "Experience Distribution":
        plot_experience_distribution(df)
    elif visualization == "Experience vs. Performance Rating":
        plot_experience_vs_performance_rating(df)
    elif visualization == "Performance Rating by Years of Experience":
        plot_performance_rating_by_yoe()
    elif visualization == "Top 10 Skills":
        plot_top_skills(df)


def contact_us_page():
    st.image("pictures/full logo.png", use_column_width=True)

    st.header(":mailbox: Let's Connect!")
    contact_form = """
    <form action="https://formsubmit.co/mishraaipsitaa702@gmail.com" method="POST">
         <input type="hidden" name="_captcha" value="false">
         <input type="text" name="name" placeholder="Your name" required>
         <input type="email" name="email" placeholder="Your email" required>
         <textarea name="message" placeholder="Your message here"></textarea>
         <button type="submit">Send</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)
    local_css("style.css")

def main():
    # Main navigation logic
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Team Segmentation Tool", "Data Analysis", "Task Monitoring Tool", "Contact Us"])
    if page == "Home":
        main_page()
    elif page == "Team Segmentation Tool":
        team_segmentation_page()
    elif page == "Data Analysis":
        data_analysis_page()
    elif page == "Task Monitoring Tool":
        task_monitoring_page()
    elif page == "Contact Us":
        contact_us_page()

if __name__ == "__main__":
    main()
