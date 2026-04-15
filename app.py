import streamlit as st
import pandas as pd
import plotly.express as px
from src.config import SKILLS, SKILL_MATRIX_PATH, CLEANED_DATA_PATH
from src.salary_gap_analyzer import calculate_salary_gap
from src.role_fit_analyzer import calculate_role_fit
from src.career_recommendation import career_skill_gap, ROLE_SUGGESTED_SKILLS, ROLE_CATEGORY_MAP
from src.salary_analysis import salary_by_skill, salary_by_skill_for_role
from src.network_analysis import build_network, build_network_for_role
from src.recommendation_engine import recommend_skills

st.set_page_config(page_title="DataAnalytics Career Hub", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .recommendation-card {
        background: #1e2130; padding: 16px 20px; border-radius: 10px;
        margin-bottom: 12px; border-left: 5px solid #00d2ff; transition: transform 0.2s;
    }
    .recommendation-card:hover { transform: translateX(4px); }
    .role-card {
        background: #1e2130; padding: 18px 20px; border-radius: 10px;
        margin-bottom: 12px; border-top: 4px solid #ff4b4b; transition: transform 0.2s;
    }
    .role-card:hover { transform: translateY(-2px); }
    .skill-tag {
        display: inline-block; background: #00d2ff22; color: #00d2ff;
        border: 1px solid #00d2ff55; padding: 4px 12px; border-radius: 20px;
        font-size: 0.85em; font-weight: 600; margin: 3px;
    }
    .missing-tag {
        display: inline-block; background: #ff4b4b22; color: #ff4b4b;
        border: 1px solid #ff4b4b55; padding: 4px 12px; border-radius: 20px;
        font-size: 0.85em; font-weight: 600; margin: 3px;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("🧭 Navigation")
    selected_feature = st.radio("📌 Select Feature", [
        "🌐 Skill Network & Demand",
        "💵 Salary by Skill",
        "💡 Next Skill Recommender",
        "📈 Job Role Skill Gap",
        "💰 Salary Gap Analyzer",
        "🎯 Role Fit Quiz"
    ])
    st.markdown("---")
    st.header("🎯 Target Job Title")
    target_role = st.selectbox("Select your target role:", [
        "Data Analyst", "Data Scientist", "Data Engineer",
        "Business Analyst", "Senior Analyst", "Junior Analyst", "Technical Analyst"
    ])

job_category = ROLE_CATEGORY_MAP.get(target_role, target_role)

st.title("🚀 DataAnalytics Career Hub")
st.markdown("A **personalized career analytics tool** — find your skill gaps, best-fit roles, and salary targets.")
st.markdown("---")

suggested = ROLE_SUGGESTED_SKILLS.get(target_role, [s.capitalize() for s in SKILLS[:10]])
current_skills_display = st.multiselect(
    f"🛠️ Your current skills (suggested for **{target_role}** — search for any skill):",
    options=[s.capitalize() for s in SKILLS],
    default=suggested[:3]
)
current_skills = [s.lower() for s in current_skills_display]

st.markdown("---")

if selected_feature == "🌐 Skill Network & Demand":
    st.header(f"🌐 Skill Network & Demand — {target_role}")
    col1, col2 = st.columns([1, 2])

    with col1:
        view_mode = st.radio("Show skills for:", ["Top 15 (All Skills)", "My Selected Skills Only"])
        analyze_btn = st.button("Analyze Demand", type="primary", use_container_width=True)
        st.caption(f"Data filtered to **{target_role}** job postings.")

    with col2:
        if analyze_btn:
            with st.spinner(f"Building network for {target_role}..."):
                try:
                    _, centrality = build_network_for_role(job_category)

                    if not centrality:
                        st.warning(f"Not enough data for {target_role}.")
                    else:
                        cent_df = pd.DataFrame.from_dict(centrality, orient="index", columns=["Centrality"]).reset_index()
                        cent_df.columns = ["Skill", "Centrality"]
                        cent_df["Skill_lower"] = cent_df["Skill"].str.lower()

                        if view_mode == "My Selected Skills Only" and current_skills:
                            cent_df = cent_df[cent_df["Skill_lower"].isin(current_skills)]
                            title = f"Your Skills — Demand in {target_role} Postings"
                        else:
                            cent_df = cent_df.sort_values("Centrality", ascending=False).head(15)
                            title = f"Top 15 In-Demand Skills for {target_role}"

                        cent_df["Skill"] = cent_df["Skill"].str.capitalize()
                        cent_df["You Have"] = cent_df["Skill_lower"].isin(current_skills)
                        cent_df["Label"] = cent_df.apply(
                            lambda r: f"{r['Skill']} ⭐" if r["You Have"] else r["Skill"], axis=1
                        )
                        cent_df = cent_df.sort_values("Centrality", ascending=False)

                        fig = px.bar(
                            cent_df, x="Centrality", y="Label", orientation="h",
                            title=title,
                            color="You Have",
                            color_discrete_map={True: "#FFD700", False: "#7B2FBE"}
                        )
                        fig.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)

                        my_in_top = cent_df[cent_df["You Have"]]["Skill"].tolist()
                        if my_in_top:
                            st.success(f"✅ Your skills here: **{', '.join(my_in_top)}**")
                        else:
                            st.info("None of your selected skills appear in this view.")
                except Exception as e:
                    st.error(f"Error: {e}")

elif selected_feature == "💵 Salary by Skill":
    st.header(f"💵 Salary by Skill — {target_role}")
    col1, col2 = st.columns([1, 2])

    with col1:
        view_mode = st.radio("Show salaries for:", ["Top 15 (All Skills)", "My Selected Skills Only"])
        sal_btn = st.button("Analyze Salaries", type="primary", use_container_width=True)
        st.caption(f"Data filtered to **{target_role}** job postings.")

    with col2:
        if sal_btn:
            with st.spinner(f"Calculating salaries for {target_role}..."):
                try:
                    salary_df = salary_by_skill_for_role(job_category).reset_index()
                    salary_df.columns = ["Skill", "Average Salary ($K)"]
                    salary_df = salary_df.dropna()
                    salary_df["Skill_lower"] = salary_df["Skill"].str.lower()

                    if view_mode == "My Selected Skills Only" and current_skills:
                        salary_df = salary_df[salary_df["Skill_lower"].isin(current_skills)]
                        title = f"Your Skills — Average Salary in {target_role}"
                    else:
                        salary_df = salary_df.sort_values("Average Salary ($K)", ascending=False).head(15)
                        title = f"Top 15 Highest Paying Skills for {target_role}"

                    salary_df["Skill"] = salary_df["Skill"].str.capitalize()
                    salary_df["You Have"] = salary_df["Skill_lower"].isin(current_skills)
                    salary_df["Label"] = salary_df.apply(
                        lambda r: f"{r['Skill']} ⭐" if r["You Have"] else r["Skill"], axis=1
                    )

                    if salary_df.empty:
                        st.warning("No salary data found for this selection.")
                    else:
                        fig = px.bar(
                            salary_df, x="Label", y="Average Salary ($K)",
                            title=title,
                            color="You Have",
                            color_discrete_map={True: "#FFD700", False: "#c44e52"}
                        )
                        fig.update_layout(showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)

                        my_in_top = salary_df[salary_df["You Have"]]["Skill"].tolist()
                        if my_in_top:
                            st.success(f"✅ Your skills shown: **{', '.join(my_in_top)}**")
                        else:
                            st.info("None of your selected skills appear in this view.")
                except Exception as e:
                    st.error(f"Error: {e}")

elif selected_feature == "💡 Next Skill Recommender":
    st.header("💡 Next Skill to Learn")
    col1, col2 = st.columns([1, 2])
    with col1:
        top_n = st.slider("Number of recommendations", 1, 10, 5)
        srec_btn = st.button("Predict Next Skill", type="primary", use_container_width=True)

    with col2:
        if srec_btn:
            if not current_skills:
                st.warning("Please add some skills above first.")
            else:
                with st.spinner("Calculating..."):
                    try:
                        recs = recommend_skills(SKILL_MATRIX_PATH, current_skills, top_n)
                        if recs:
                            rec_df = pd.DataFrame(recs, columns=["Skill", "Co-occurrence Score"])
                            rec_df["Skill"] = rec_df["Skill"].str.capitalize()
                            fig = px.pie(rec_df, values="Co-occurrence Score", names="Skill",
                                         title="Best Skills to Add to Your Profile", hole=0.4)
                            st.plotly_chart(fig, use_container_width=True)
                            st.markdown("**These skills appear most frequently alongside the skills you already have.**")
                        else:
                            st.info("No recommendations found. Try selecting different skills.")
                    except Exception as e:
                        st.error(f"Error: {e}")

elif selected_feature == "📈 Job Role Skill Gap":
    st.header(f"📈 Skill Gap: Becoming a **{target_role}**")
    st.write(f"See exactly which top skills are required for **{target_role}** and which ones you're missing.")
    col1, col2 = st.columns([1, 2])
    with col1:
        gap_btn = st.button("Calculate Skill Gap", type="primary", use_container_width=True)

    with col2:
        if gap_btn:
            if not current_skills:
                st.warning("Please add some skills above first.")
            else:
                with st.spinner(f"Analyzing gaps for {target_role}..."):
                    try:
                        result = career_skill_gap(CLEANED_DATA_PATH, current_skills, target_role)
                        if "error" in result:
                            st.error(result["error"])
                        else:
                            req = result["Required Skills"]
                            you_have = [s for s in current_skills if s in req]
                            missing = result["Skills To Learn"]
                            match_pct = (len(you_have) / len(req)) * 100 if req else 0

                            st.metric(f"Your match for {target_role}", f"{match_pct:.0f}%")
                            st.progress(match_pct / 100)
                            st.markdown("---")

                            skill_status = [{"Skill": s.capitalize(), "Status": "✅ You Have" if s in you_have else "❌ Missing"} for s in req]
                            df_status = pd.DataFrame(skill_status)
                            fig = px.bar(df_status, x="Skill", color="Status",
                                         title=f"Required vs Your Skills for {target_role}",
                                         color_discrete_map={"✅ You Have": "#00d2ff", "❌ Missing": "#ff4b4b"})
                            st.plotly_chart(fig, use_container_width=True)

                            st.markdown("**✅ Skills You Have:**")
                            if you_have:
                                st.markdown(" ".join([f"<span class='skill-tag'>{s.capitalize()}</span>" for s in you_have]), unsafe_allow_html=True)
                            else:
                                st.write("None from the required list")

                            st.markdown("**❌ Skills to Learn:**")
                            if missing:
                                st.markdown(" ".join([f"<span class='missing-tag'>{s.capitalize()}</span>" for s in missing]), unsafe_allow_html=True)
                            else:
                                st.success(f"🎉 You already have all the core skills for {target_role}!")
                    except Exception as e:
                        st.error(str(e))

elif selected_feature == "💰 Salary Gap Analyzer":
    st.header("💰 Salary Gap Analyzer")
    st.markdown(f"How far are you from your salary target as a **{target_role}**?")
    col1, col2 = st.columns([1, 2])
    with col1:
        target_salary = st.number_input("Enter your target salary ($)", min_value=30000, max_value=500000, value=90000, step=5000)
        st.info(f"Based on your target role: **{target_role}**")
        analyze_btn = st.button("Analyze Salary Gap", type="primary", use_container_width=True)

    with col2:
        if analyze_btn:
            if not current_skills:
                st.warning("Please add some skills above first.")
            else:
                with st.spinner("Analyzing market data..."):
                    try:
                        result = calculate_salary_gap(current_skills, target_salary)
                        if result["gap"] <= 0:
                            st.success(result["message"])
                        else:
                            c1, c2, c3 = st.columns(3)
                            c1.metric("Your Est. Salary", f"${result['current_salary']:.1f}K")
                            c2.metric("Target Salary", f"${result['target_salary']:.0f}K")
                            c3.metric("Gap to Close", f"${result['gap']:.1f}K", delta=f"-${result['gap']:.1f}K", delta_color="inverse")

                            st.markdown("### 💡 Top Skills to Add for a Pay Bump")
                            if result["recommendations"]:
                                df_chart = pd.DataFrame(result["recommendations"])
                                df_chart["skill"] = df_chart["skill"].str.capitalize()
                                fig = px.bar(df_chart, x="skill", y="boost",
                                             title="Salary Boost by Adding Each Skill ($K)",
                                             labels={"boost": "Salary Boost ($K)", "skill": "Skill"},
                                             color="boost", color_continuous_scale="Blues")
                                st.plotly_chart(fig, use_container_width=True)
                                for rec in result["recommendations"]:
                                    st.markdown(f"""
                                    <div class="recommendation-card">
                                        <b style="color:#00d2ff;">{rec['skill'].capitalize()}</b>
                                        <span style="color:#4CAF50; margin-left:8px;">(+${rec['boost']:.1f}K)</span>
                                        <p style="margin:6px 0 0; color:#ccc;">Raises avg salary to <strong>${rec['new_salary']:.1f}K</strong></p>
                                    </div>
                                    """, unsafe_allow_html=True)
                            else:
                                st.info("No single missing skill clearly bumps your average above the target. Keep adding skills!")
                    except Exception as e:
                        st.error(str(e))

elif selected_feature == "🎯 Role Fit Quiz":
    st.header("🎯 Role Fit Quiz")
    st.markdown("We scan all job categories and score how well your skill set matches each one.")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.write("Your skills from above will be used to calculate fit scores across all roles.")
        fit_btn = st.button("Calculate My Role Fit", type="primary", use_container_width=True)

    with col2:
        if fit_btn:
            if not current_skills:
                st.warning("Please add some skills above first.")
            else:
                with st.spinner("Scanning all job categories..."):
                    try:
                        fit_result = calculate_role_fit(current_skills)
                        if "error" in fit_result:
                            st.error(fit_result["error"])
                        elif fit_result["role_fits"]:
                            top = fit_result["role_fits"][0]
                            st.success(f"### 🎉 Best Match: **{top['role']}** ({top['fit_score']}% fit)")

                            df_fit = pd.DataFrame(fit_result["role_fits"])
                            df_fit = df_fit[df_fit["fit_score"] > 0]
                            fig = px.bar(df_fit, x="fit_score", y="role", orientation="h",
                                         title="Your Fit Score Across All Data Roles (%)",
                                         labels={"fit_score": "Fit Score (%)", "role": "Role"},
                                         color="fit_score", color_continuous_scale="Viridis")
                            fig.update_layout(yaxis={"categoryorder": "total ascending"})
                            st.plotly_chart(fig, use_container_width=True)

                            st.markdown("### Detailed Breakdown")
                            for fit in fit_result["role_fits"]:
                                if fit["fit_score"] > 0:
                                    color = "#00d2ff" if fit["fit_score"] > 70 else "#ffa500" if fit["fit_score"] > 40 else "#ff4b4b"
                                    st.markdown(f"""
                                    <div class="role-card">
                                        <div style="display:flex; justify-content:space-between; align-items:center;">
                                            <b style="font-size:1.1em;">{fit['role']}</b>
                                            <span style="color:{color}; font-weight:700; font-size:1.1em;">{fit['fit_score']}%</span>
                                        </div>
                                        <p style="margin:8px 0 4px; color:#aaa; font-size:0.85em;">Key skills for this role:</p>
                                        <div>{''.join([f'<span class="skill-tag">{s.capitalize()}</span>' for s in fit["key_skills"]])}</div>
                                    </div>
                                    """, unsafe_allow_html=True)
                        else:
                            st.warning("No matching roles found.")
                    except Exception as e:
                        st.error(str(e))
