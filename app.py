import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import altair as alt

st.set_page_config(layout="centered")
st.title("Center for Success: Social Media Marketing Analytics Dashboard")


@st.cache_data
def load_data():
    email_clicks = pd.read_csv("email_clicks.csv")
    email_overview = pd.read_csv("email_overview.csv")
    meta_suite_df = pd.read_excel("Instagram_meta_business_suite.xlsx")
    insta_insights_summary = pd.read_excel("Final_Instagram_Insights_Data.xlsx")
    fb_df = pd.read_csv("facebook_published.csv")
    followers_df = pd.read_excel("Linkedin_followers.xlsx")
    visitors_df = pd.read_excel("linkedin_visitors.xlsx")
    activity_df = pd.read_excel("LinkedIn.xlsx")
    competitors_df = pd.read_excel("competitors_linkedin.xlsx")
    return (
        email_clicks,
        email_overview,
        meta_suite_df,
        insta_insights_summary,
        fb_df,
        followers_df,
        visitors_df,
        activity_df,
        competitors_df,
    )


(
    email_clicks,
    email_overview,
    meta_suite_df,
    insta_insights_summary,
    fb_df,
    followers_df,
    visitors_df,
    activity_df,
    competitors_df,
) = load_data()

# --- Top Panel Navigation ---
page = st.selectbox(
    "Select Analysis Section",
    ("Email Marketing", "Instagram", "Facebook", "LinkedIn", "Cross-Platform Overview"),
)

# ============ EMAIL MARKETING ============
if page == "Email Marketing":
    st.header("Email Marketing Performance")

    st.subheader("What days of the week are best for sending emails?")

    email_clicks["Time Sent"] = pd.to_datetime(email_clicks["Time Sent"])
    email_clicks["Open Rate (%)"] = (
        email_clicks["Open Rate"].str.replace("%", "").astype(float)
    )
    email_clicks["Click Rate (%)"] = (
        email_clicks["Click Rate"].str.replace("%", "").astype(float)
    )
    email_clicks["Day of Week"] = email_clicks["Time Sent"].dt.day_name()

    # Open and Click Rate by Day
    dow_summary = (
        email_clicks.groupby("Day of Week")[["Open Rate (%)", "Click Rate (%)"]]
        .mean()
        .reindex(
            [
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
                "Sunday",
            ]
        )
    )
    import altair as alt

    dow_reset = dow_summary.reset_index().melt(
        id_vars="Day of Week", var_name="Rate Type", value_name="Rate"
    )
    bar_chart = (
        alt.Chart(dow_reset)
        .mark_bar()
        .configure_view(stroke=None)
        .configure_axis(grid=False, domain=False, title=None)
        .encode(
            x=alt.X(
                "Day of Week:N",
                sort=[
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ],
                axis=alt.Axis(labelAngle=-45),
            ),
            y="Rate:Q",
            color="Rate Type:N",
            tooltip=["Day of Week", "Rate Type", "Rate"],
            column=alt.Column("Rate Type:N", spacing=10, title=None),
        )
        .properties(width=300, height=400)
        .encode(
            x=alt.X(
                "Day of Week:N",
                sort=[
                    "Monday",
                    "Tuesday",
                    "Wednesday",
                    "Thursday",
                    "Friday",
                    "Saturday",
                    "Sunday",
                ],
                axis=alt.Axis(labelAngle=-45),
            ),
            y="Rate:Q",
            color="Rate Type:N",
            tooltip=["Day of Week", "Rate Type", "Rate"],
        )
        .properties(width=250, height=200)
    )
    st.altair_chart(bar_chart, use_container_width=False)

    st.markdown(
        "Engagement is consistently stronger on Wednesdays and Thursdays, with both open and click rates peaking midweek. This suggests that audiences are more responsive during these days, likely due to routine checking of email midweek. We should prioritize scheduling important email campaigns for midweek delivery to maximize impact."
    )

    # Time trend
    st.subheader("How have our email open and click rates changed over time?")
    line_data = email_clicks[["Time Sent", "Open Rate (%)", "Click Rate (%)"]].melt(
        id_vars="Time Sent", var_name="Rate Type", value_name="Rate"
    )
    line_chart = (
        alt.Chart(line_data)
        .mark_line(point=True)
        .configure_view(stroke=None)
        .configure_axis(grid=False, domain=False, title=None)
        .encode(
            x=alt.X("Time Sent:T", axis=alt.Axis(labelAngle=-45)),
            y="Rate:Q",
            color="Rate Type:N",
            tooltip=["Time Sent:T", "Rate Type:N", "Rate:Q"],
        )
        .interactive()
        .properties(width=700, height=400)
    )
    st.altair_chart(line_chart, use_container_width=False)

    st.markdown(
        "There’s a noticeable rise in click and open rates during campaign bursts in late December and early March. This suggests that time-sensitive or seasonal content (e.g., year-end wrap-ups or events like March Book Madness) significantly boosts engagement. Scheduling similar campaigns in key periods could improve performance."
    )

    # Top campaigns
    st.subheader(
        "Which email campaigns had the highest click and open rates, and what made them successful?"
    )
    col1, col2 = st.columns(2)

    top_open = email_clicks.sort_values(by="Open Rate (%)", ascending=False)[
        ["Campaign Name", "Open Rate (%)"]
    ].head(10)
    top_click = email_clicks.sort_values(by="Click Rate (%)", ascending=False)[
        ["Campaign Name", "Click Rate (%)"]
    ].head(10)

    open_chart = (
        alt.Chart(top_open, title="Top 10 Open Rates")
        .mark_bar()
        .encode(
            x=alt.X("Open Rate (%):Q", title=None),
            y=alt.Y(
                "Campaign Name:N", sort="-x", title=None, axis=alt.Axis(labelLimit=0)
            ),
            tooltip=["Campaign Name:N", "Open Rate (%):Q"],
        )
        .properties(width=350, height=300)
        .configure_view(stroke=None)
        .configure_axis(grid=False, domain=False, title=None)
        .configure_title(anchor="middle")
    )

    click_chart = (
        alt.Chart(top_click, title="Top 10 Click Rates")
        .mark_bar(color="orange")
        .encode(
            x=alt.X("Click Rate (%):Q", title=None),
            y=alt.Y(
                "Campaign Name:N", sort="-x", title=None, axis=alt.Axis(labelLimit=0)
            ),
            tooltip=["Campaign Name:N", "Click Rate (%):Q"],
        )
        .properties(width=350, height=300)
        .configure_view(stroke=None)
        .configure_axis(grid=False, domain=False, title=None)
        .configure_title(anchor="middle")
    )

    col1, col2 = st.columns(2)
    with col1:
        st.altair_chart(open_chart, use_container_width=False)
    with col2:
        st.altair_chart(click_chart, use_container_width=False)

    st.markdown(
        'Campaigns with high open rates don\'t always guarantee high click rates. For instance, "[Reminder] Party for Langston" had a strong open rate but low clicks, suggesting interest didn\'t translate into action. By contrast, the "EOY 2024" emails show consistent performance across both metrics.'
    )

    st.subheader("Summary")
    st.markdown(
        """
    - Over the past few months, our email campaigns have shown encouraging trends in engagement, particularly during key periods like year-end (EOY) and event-driven campaigns (e.g., March Book Madness). Open rates have consistently hovered around 40–50%, with click rates peaking above 15–17% for the best-performing campaigns.

    - High-performing campaigns not only had engaging subject lines but were also time-sensitive, seasonal, or event-focused, indicating that urgency and relevance are strong motivators for our audience.

    - Our analysis also revealed that Wednesdays and Thursdays are the most effective days for sending emails, suggesting that timing plays a critical role in campaign performance.
    """
    )

    st.subheader("Recommendations")
    st.markdown(
        """
    1. **Send Emails Midweek**:
    Try sending important emails on Wednesdays or Thursdays. These days tend to get better attention and more clicks.

    2. **Repeat What Worked Well**:
    Look at past successful emails like the EOY 2024 and March Book Madness campaigns. Use similar styles or formats in future emails.

    3. **Use Timely Topics**:
    Plan emails around holidays, seasons, or special events. These types of emails usually get more people to open and click.

    4. **Write Better Subject Lines**:
    Keep subject lines short, clear, and to the point. It helps to test a few versions to see which one gets more opens.

    5. **Clean Up the Email List**:
    Some emails bounced because the addresses weren’t valid. It’s a good idea to double-check the list every now and then so we’re not emailing bad addresses.

    6. **Make It Easy to Click**:
    The best emails had a clear message and one strong button or link. Try to include just one thing you want people to do.
    """
    )


# ============ INSTAGRAM ============
elif page == "Instagram":
    st.header("Instagram Performance")
    st.subheader("Overview")
    st.markdown(
        """
    - **High Visibility, Moderate Engagement**: The account reached 1,279 users, but only 82 users actually engaged (likes, comments, saves, etc.). This suggests there’s good visibility, but opportunities to increase active engagement—possibly through stronger CTAs or more interactive content.
    - **Reels Are Seen, but Not Acted On**: Reel Reach (446) is about 46% of Post Reach (978), but Reel Interactions are only 19. This indicates that while people are watching Reels, they’re not interacting much. Adding polls, questions, or clearer CTAs may help.
    - **Strong Profile Conversion**: 281 profile actions, of which 266 were profile visits, shows a high conversion rate from content to curiosity. This is a good sign that content is motivating viewers to learn more.
    - **Stories are Underperforming**: Story Reach (215) and Story Interactions (13) are low compared to posts and reels. Stories could be optimized with more interactive elements like stickers, questions, or polls.
    - **Most Engagement Comes from Followers**: While most reach comes from non-followers, engagement is mostly from followers (69 out of 82). This means while content is discoverable, only followers are actively engaging—so there may be a need to make content more engaging for new viewers.
    """
    )

    st.subheader(
        "What kind of content drives the most reach and engagement on Instagram?"
    )

    meta_suite_df.columns = (
        meta_suite_df.columns.str.strip().str.lower().str.replace(" ", "_")
    )
    type_perf = (
        meta_suite_df.groupby("post_type")[
            ["reach", "likes", "comments", "shares", "views"]
        ]
        .mean()
        .sort_values(by="reach", ascending=False)
        .reset_index()
    )

    import altair as alt

    bar_chart = (
        alt.Chart(type_perf)
        .mark_bar()
        .configure_view(stroke=None)
        .configure_axis(grid=False, domain=False, title=None)
        .encode(
            x=alt.X("reach:Q", title="Average Reach"),
            y=alt.Y("post_type:N", sort="-x", title=None),
            tooltip=["post_type:N", "reach:Q"],
        )
        .properties(width=600, height=300)
    )
    st.altair_chart(bar_chart, use_container_width=False)

    st.markdown(
        "IG image posts currently generate the highest reach on average. Carousels and other formats have slightly lower engagement. Maintaining a strong focus on image posts is effective, but experimenting more with carousels and videos could help uncover additional high-performing formats."
    )

    st.subheader("When is the best time to post to get the most interaction?")

    meta_suite_df["publish_time"] = pd.to_datetime(meta_suite_df["publish_time"])
    meta_suite_df["hour"] = meta_suite_df["publish_time"].dt.hour
    meta_suite_df["weekday"] = pd.Categorical(
        meta_suite_df["publish_time"].dt.day_name(),
        categories=[
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ],
        ordered=True,
    )

    heatmap_data = (
        meta_suite_df.groupby(["weekday", "hour"])["reach"].mean().reset_index()
    )
    heatmap_chart = (
        alt.Chart(heatmap_data)
        .mark_rect()
        .configure_view(stroke=None)
        .configure_axis(grid=False, domain=False, title=None)
        .encode(
            x=alt.X("hour:O", title="Hour of Day", axis=alt.Axis(labelAngle=0)),
            y=alt.Y("weekday:N", title=None),
            color=alt.Color("reach:Q", scale=alt.Scale(scheme="blues")),
            tooltip=["weekday:N", "hour:O", "reach:Q"],
        )
        .properties(width=600, height=400)
    )

    st.altair_chart(heatmap_chart, use_container_width=False)

    st.markdown(
        "Tuesday at 12 PM is the best-performing slot overall. Additionally, early mornings on Monday and Wednesday consistently show strong reach, suggesting these days are ideal for posting important updates or content."
    )

    st.subheader("What content topics lead to high engagement?")

    meta_suite_df["description"].fillna("", inplace=True)
    keywords = [
        "book",
        "madness",
        "eoy",
        "party",
        "langston",
        "march",
        "event",
        "read",
        "donate",
        "celebrate",
        "invited",
        "register",
    ]
    for kw in keywords:
        meta_suite_df[kw] = (
            meta_suite_df["description"].str.lower().str.contains(kw).astype(int)
        )

    theme_engagement = meta_suite_df[
        keywords + ["reach", "likes", "comments", "shares", "views"]
    ].copy()
    theme_flags = theme_engagement.melt(
        id_vars=["reach", "likes", "comments", "shares", "views"],
        var_name="theme",
        value_name="flag",
    )
    theme_stats = (
        theme_flags[theme_flags["flag"] == 1]
        .groupby("theme")[["reach", "likes", "comments", "shares", "views"]]
        .mean()
        .sort_values(by="reach", ascending=False)
        .reset_index()
    )

    theme_chart = (
        alt.Chart(theme_stats)
        .mark_bar()
        .configure_view(stroke=None)
        .configure_axis(grid=False, domain=False, title=None)
        .encode(
            x=alt.X("reach:Q", title="Average Reach"),
            y=alt.Y("theme:N", sort="-x", title=None),
            tooltip=["theme:N", "reach:Q"],
        )
        .properties(width=600, height=400)
    )

    st.altair_chart(theme_chart, use_container_width=False)

    st.markdown(
        'Words like "celebrate", "community", "thankful", and "event" appear frequently in high-engagement posts. This reinforces the idea that posts centered around gratitude, recognition, and shared moments resonate strongly with the audience.'
    )

    st.subheader("Summary")
    st.markdown(
        """
    - 1,279 Accounts Reached — strong visibility overall
    - Reels are the Top-Performing Format, averaging 196 reach per post
    - Majority of Reach (73%) came from Non-Followers, showing good discoverability
    - Only 6% of Reach Converted to Engagement, indicating room to improve interaction
    - Best posting times: Tuesdays at 12 PM, and early weekday mornings
    - Top-performing themes: “Event”, “Party”, and “Celebrate”-style content
    """
    )

    st.subheader("Recommendations")
    st.markdown(
        """
    1. **Prioritize Reels in Your Content Strategy**: Reels deliver the highest reach and should be posted regularly. Use trending audio, captions, and call-to-actions to maximize their performance.
    2. **Post During High-Engagement Windows**: Focus on Tuesdays at 12 PM and weekday mornings, when your audience is most active.
    3. **Boost Engagement with CTAs and Interactivity**: Encourage more actions by adding polls, questions, and “comment below” prompts—especially in Reels and Stories.
    4. **Double Down on Event-Focused Content**: Posts referencing events, parties, or Langston campaigns consistently perform well. Plan content around similar high-interest topics.
    5. **Optimize Profile for Conversions**: With 266 profile visits in 90 days, make sure your bio and pinned posts encourage visitors to follow and explore further.
    6. **Refresh Story Strategy**: Stories are underperforming. Try using interactive stickers, countdowns, and behind-the-scenes content to revive engagement.
    """
    )

# ============ FACEBOOK ============

elif page == "Facebook":
    st.header("Facebook Performance")

    st.subheader("Which Facebook posts had the highest engagement?")
    fb_df.columns = fb_df.columns.str.strip().str.lower().str.replace(" ", "_")
    fb_df["reactions"] = fb_df["reactions"].fillna(0)
    fb_df["comments"] = fb_df["comments"].fillna(0)
    fb_df["shares"] = fb_df["shares"].fillna(0)
    fb_df["total_engagement"] = fb_df["reactions"] + fb_df["comments"] + fb_df["shares"]

    top_engaged_posts = fb_df.sort_values(by="total_engagement", ascending=False)[
        ["title", "post_type", "reactions", "comments", "shares", "total_engagement"]
    ].head(10)

    # Generate and display word cloud
    text_blob = " ".join(top_engaged_posts["title"].astype(str))
    wordcloud = WordCloud(
        width=800, height=300, background_color="white", colormap="Blues"
    ).generate(text_blob)
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig, use_container_width=True)

    st.markdown(
        "Photos generate the highest engagement across all metrics — reactions, comments, and shares. Link posts lag behind in every category. This suggests that focusing on visual storytelling through images is the most effective way to connect with your Facebook audience."
    )

    st.subheader("What types of posts are most effective?")
    type_summary = (
        fb_df.groupby("post_type")[["reactions", "comments", "shares"]]
        .mean()
        .reset_index()
    )
    type_summary_melted = type_summary.melt(
        id_vars="post_type", var_name="Metric", value_name="Average"
    )

    bar_chart = (
        alt.Chart(type_summary_melted)
        .mark_bar()
        .configure_view(stroke=None)
        .configure_axis(grid=False, domain=False, title=None)
        .encode(
            x=alt.X("Metric:N", title=None, axis=alt.Axis(labelAngle=-45)),
            y=alt.Y("Average:Q", title="Average Engagement"),
            color=alt.Color("Metric:N"),
            column=alt.Column("post_type:N", title=None, spacing=10),
            tooltip=["post_type:N", "Metric:N", "Average:Q"],
        )
        .properties(width=150, height=400)
    )
    st.altair_chart(bar_chart, use_container_width=False)
    st.markdown(
        "Photos are the most engaging format, outperforming other types in reactions, comments, and shares. Top-performing posts feature gratitude, celebration, and community-focused content. Engagement peaked on select dates, indicating that event or milestone-based posts resonate strongly."
    )

    st.subheader("Summary")
    st.markdown(
        """
    - **Photos are the most engaging format**, outperforming other types in reactions, comments, and shares
    - **Top-performing posts** feature gratitude, celebration, and community-focused content
    - **Engagement peaked on select dates**, indicating that event or milestone-based posts resonate strongly
    - **Click behavior is moderate**, with most clicks coming from general post interactions, followed by link and photo clicks
    - **Most posts do not trigger high link click activity**, suggesting CTAs could be stronger
    """
    )

    st.subheader("Recommendations to boost reach and interaction")
    st.markdown(
        """
    1. **Use More Photo-Based Posts**: Continue prioritizing photos, as they consistently deliver the highest engagement across metrics.
    2. **Tell Stories That Celebrate People & Moments**: Focus on posts that highlight individuals, gratitude, or achievements. These resonate well with the audience.
    3. **Include Clear, Visual Call-to-Actions (CTAs)**: To increase clicks and conversions, use buttons, short links, or captions that say exactly what to do (e.g., “Click to register”).
    4. **Post Around Events or Key Moments**: Engagement spikes around event-related posts. Create content tied to holidays, program launches, or celebrations.
    5. **Optimize for Interaction, Not Just Awareness**: Use interactive tools (polls, questions) and captions that invite comments or shares, not just views.
    6. **Review and Repurpose High-Performing Posts**: Identify top posts and reuse their structure or message. Consider boosting them through ads for even greater reach.
    """
    )

# ============ LINKEDIN ============

elif page == "LinkedIn":
    st.header("LinkedIn Performance")

    st.subheader("How is the growth of the LinkedIn page?")
    followers_df.columns = followers_df.columns.str.strip()
    followers_df["Date"] = pd.to_datetime(followers_df["Date"], errors="coerce")
    followers_df["Total followers"] = pd.to_numeric(
        followers_df["Total followers"], errors="coerce"
    )

    follower_trend = followers_df[["Date", "Total followers"]].dropna()

    line_chart = (
        alt.Chart(follower_trend)
        .mark_line(point=True)
        .configure_view(stroke=None)
        .configure_axis(grid=False, domain=False)
        .encode(
            x=alt.X(
                "Date:T", axis=alt.Axis(labelAngle=-45, format="%b %d", title=None)
            ),
            y="Total followers:Q",
            tooltip=["Date:T", "Total followers:Q"],
        )
        .properties(width=600, height=300)
    )
    st.altair_chart(line_chart, use_container_width=False)

    st.markdown(
        "While the follower base is growing, the pace is relatively slow. This suggests that growth is organic and would benefit from more cross-promotion, collaboration tags, and follow prompts across platforms."
    )

    st.subheader("What kinds of posts are driving the most engagement?")
    activity_df.columns = activity_df.iloc[0]
    activity_df = activity_df.drop(index=0).reset_index(drop=True)
    activity_df.columns.name = None
    activity_df.rename(columns={activity_df.columns[0]: "Date"}, inplace=True)
    activity_df["Date"] = pd.to_datetime(activity_df["Date"], errors="coerce")

    engagement_cols = [
        "Impressions (total)",
        "Clicks (total)",
        "Reactions (total)",
        "Comments (total)",
        "Reposts (total)",
    ]
    for col in engagement_cols:
        activity_df[col] = pd.to_numeric(activity_df[col], errors="coerce")

    activity_df["Total Engagement"] = (
        activity_df["Clicks (total)"]
        + activity_df["Reactions (total)"]
        + activity_df["Comments (total)"]
        + activity_df["Reposts (total)"]
    )

    impressions_line = activity_df.copy()
    impressions_line["Metric"] = "Impressions"
    impressions_line.rename(columns={"Impressions (total)": "Value"}, inplace=True)

    engagement_line = activity_df.copy()
    engagement_line["Metric"] = "Engagement"
    engagement_line.rename(columns={"Total Engagement": "Value"}, inplace=True)

    combined = pd.concat(
        [
            impressions_line[["Date", "Value", "Metric"]],
            engagement_line[["Date", "Value", "Metric"]],
        ]
    )

    line_chart = (
        alt.Chart(combined)
        .mark_line(point=True)
        .encode(
            x=alt.X("Date:T", axis=alt.Axis(labelAngle=-45, format="%b %d")),
            y=alt.Y("Value:Q", title=None),
            color=alt.Color(
                "Metric:N",
                scale=alt.Scale(
                    domain=["Impressions", "Engagement"], range=["#1179b0", "orange"]
                ),
            ),
            tooltip=["Date:T", "Metric:N", "Value:Q"],
        )
        .configure_view(stroke=None)
        .configure_axis(grid=False, domain=False, title=None)
        .properties(width=600, height=300)
    )
    st.altair_chart(line_chart, use_container_width=False)

    st.markdown(
        "There’s a gap between visibility and interaction. To increase engagement, posts need to include clear value, calls to action, and audience-relevant content such as success stories, photos, or event coverage."
    )

    st.subheader("What is the demographic profile of our visitors?")
    visitor_summary = (
        visitors_df[
            [
                "Date",
                "Overview page views (total)",
                "Life page views (total)",
                "Jobs page views (total)",
            ]
        ]
        .copy()
        .dropna()
    )
    visitor_melted = visitor_summary.melt(
        id_vars="Date", var_name="Page Section", value_name="Views"
    )

    line_chart = (
        alt.Chart(visitor_melted)
        .mark_line(point=True)
        .configure_view(stroke=None)
        .configure_axis(grid=False, domain=False, title=None)
        .encode(
            x=alt.X("Date:T", axis=alt.Axis(labelAngle=-45, format="%b %d")),
            y="Views:Q",
            color="Page Section:N",
            tooltip=["Date:T", "Page Section:N", "Views:Q"],
        )
        .properties(width=700, height=300)
    )
    st.altair_chart(line_chart, use_container_width=False)
    st.markdown(
        "Visitors are primarily viewing the Overview section, with minimal interaction on Life or Jobs pages. This suggests an opportunity to refresh and promote these underutilized sections, potentially highlighting team culture, success stories, or available roles."
    )

    st.subheader("Are there strategies from competitors we could adopt or improve on?")
    competitors_df.columns = competitors_df.iloc[0]
    competitors_df = competitors_df.drop(index=0).reset_index(drop=True)
    competitors_df.columns.name = None
    competitors_df.rename(
        columns={
            competitors_df.columns[0]: "Organization",
            competitors_df.columns[1]: "Total Followers",
            competitors_df.columns[2]: "New Followers",
            competitors_df.columns[3]: "Total Post Engagements",
            competitors_df.columns[4]: "Total Posts",
        },
        inplace=True,
    )

    for col in [
        "Total Followers",
        "New Followers",
        "Total Post Engagements",
        "Total Posts",
    ]:
        competitors_df[col] = pd.to_numeric(competitors_df[col], errors="coerce")

    competitors_df["Engagement per Post"] = (
        competitors_df["Total Post Engagements"] / competitors_df["Total Posts"]
    )

    bar_chart = (
        alt.Chart(competitors_df)
        .mark_bar()
        .configure_view(stroke=None)
        .configure_axis(grid=False, domain=False, title=None)
        .encode(
            x=alt.X("Engagement per Post:Q", title="Engagement per Post"),
            y=alt.Y(
                "Organization:N", sort="-x", title=None, axis=alt.Axis(labelLimit=0)
            ),
            tooltip=["Organization", "Engagement per Post"],
        )
        .properties(width=700, height=300)
    )
    st.altair_chart(bar_chart, use_container_width=False)
    st.markdown(
        "High-engagement competitors post more frequently and use emotionally engaging or mission-driven content. To close the gap, Center for Success can adopt similar strategies like sharing stories, tagging partners, and posting more frequently with a strong visual identity."
    )

    st.subheader("Summary")
    st.markdown(
        """
    - **Engagement & Impressions**: Low and flat engagement despite consistent posting (90 posts in the recent period). Total reach (1,453) and total engagement (140) are disproportionate to posting effort.
    - **Visitor Behavior**: Visitors primarily view the Overview section. Life and Jobs tabs are underutilized, indicating low interest or awareness.
    """
    )

    st.subheader("Recommendations")
    st.markdown(
        """
    1. **Post Stories, Not Just Stats**: Share stories about people, milestones, or impact. Use visuals (staff photos, graphics) and keep copy tight and mission-aligned.
    2. **Repurpose High-Performing Content**: Convert top Facebook/Instagram posts into professional LinkedIn versions.
    3. **Show the Team & Partners**: Highlight staff, interns, and collaborators — this content performs well across competitors.
    4. **Promote the Life Section**: Refresh with images, short bios, or testimonials. Link to it in captions and cross-promote from email/newsletters.
    5. **Increase Posting Frequency**: Aim for 1–2 posts/week minimum. Focus on quality, consistency, and variety of content types.
    """
    )

# ============ CROSS-PLATFORM OVERVIEW ============

elif page == "Cross-Platform Overview":
    st.header("Cross-Platform Performance")

    st.subheader("Which platforms are driving the most overall value?")
    # Instagram (from insights + meta business data)
    insta_reach = 1279
    insta_engagement = 82  # interactions
    insta_profile_visits = 266
    insta_posts = 15  # estimated from recent activity

    fb_df.columns = fb_df.columns.str.strip().str.lower().str.replace(" ", "_")
    fb_df["reactions"] = fb_df["reactions"].fillna(0)
    fb_df["comments"] = fb_df["comments"].fillna(0)
    fb_df["shares"] = fb_df["shares"].fillna(0)
    fb_df["total_engagement"] = fb_df["reactions"] + fb_df["comments"] + fb_df["shares"]
    fb_reach = fb_df["reach"].sum()
    fb_engagement = fb_df["total_engagement"].sum()
    fb_posts = fb_df.shape[0]

    # LinkedIn
    activity_df.columns = activity_df.iloc[0]
    activity_df = activity_df.drop(index=0).reset_index(drop=True)
    activity_df.columns.name = None
    activity_df.rename(columns={activity_df.columns[0]: "Date"}, inplace=True)
    activity_df["Date"] = pd.to_datetime(activity_df["Date"], errors="coerce")

    engagement_cols = [
        "Impressions (total)",
        "Clicks (total)",
        "Reactions (total)",
        "Comments (total)",
        "Reposts (total)",
    ]
    for col in engagement_cols:
        activity_df[col] = pd.to_numeric(activity_df[col], errors="coerce")

    activity_df["Total Engagement"] = (
        activity_df["Clicks (total)"]
        + activity_df["Reactions (total)"]
        + activity_df["Comments (total)"]
        + activity_df["Reposts (total)"]
    )

    linkedin_reach = activity_df["Impressions (total)"].sum()
    linkedin_engagement = activity_df["Total Engagement"].sum()
    linkedin_profile_visits = visitors_df["Total unique visitors (total)"].sum()
    linkedin_posts = activity_df.shape[0]

    platform_df = pd.DataFrame(
        {
            "Platform": ["Instagram", "Facebook", "LinkedIn"],
            "Reach": [insta_reach, fb_reach, linkedin_reach],
            "Engagements": [insta_engagement, fb_engagement, linkedin_engagement],
            "Profile Visits": [insta_profile_visits, None, linkedin_profile_visits],
            "Posts": [insta_posts, fb_posts, linkedin_posts],
        }
    )

    melted_platform = platform_df.melt(
        id_vars="Platform",
        value_vars=["Reach", "Engagements", "Profile Visits"],
        var_name="Metric",
        value_name="Value",
    )

    bar_chart = (
        alt.Chart(melted_platform.dropna())
        .mark_bar()
        .configure_view(stroke=None)
        .configure_axis(grid=False, domain=False, title=None)
        .encode(
            x=alt.X("Value:Q", title=None),
            y=alt.Y("Metric:N", sort="-x", title=None, axis=alt.Axis(labels=False)),
            row=alt.Row("Platform:N", sort="ascending", title=None),
            color="Metric:N",
            tooltip=["Platform:N", "Metric:N", "Value:Q"],
        )
        .properties(width=500, height=100)
    )
    st.altair_chart(bar_chart, use_container_width=False)
    st.markdown(
        "Facebook is currently the strongest channel for reach and engagement. However, Instagram drives more profile traffic with fewer posts, while LinkedIn shows moderate performance and room for growth."
    )

    st.subheader("What campaigns worked best across all platforms?")
    campaign_df = pd.DataFrame(
        {
            "Campaign/Theme": [
                "Langston Party",
                "March Book Madness",
                "EOY Appeal",
                "Event/Celebration",
            ],
            "Facebook": ["✅", "✅", "", "✅"],
            "Instagram": ["✅", "✅", "✅", "✅"],
            "Email": ["✅", "✅", "✅", ""],
        }
    )

    heatmap = (
        alt.Chart(
            campaign_df.melt(
                id_vars="Campaign/Theme", var_name="Platform", value_name="Presence"
            )
        )
        .transform_calculate(present='datum.Presence === "✅" ? 1 : 0')
        .mark_rect()
        .encode(
            x=alt.X("Platform:N", title=None, axis=alt.Axis(labelAngle=0)),
            y=alt.Y("Campaign/Theme:N", title=None, axis=alt.Axis(labelLimit=0)),
            color=alt.Color(
                "present:Q",
                scale=alt.Scale(domain=[0, 1], range=["#ffffff", "#1179b0"]),
                legend=alt.Legend(
                    title="Presence",
                    orient="right",
                    values=[0, 1],
                    labelExpr="datum.value === 1 ? 'Yes' : 'No'",
                ),
            ),
            tooltip=["Campaign/Theme", "Platform", "Presence"],
        )
        .properties(width=600, height=300)
    )
    st.altair_chart(heatmap, use_container_width=False)
    st.markdown(
        "The most successful campaigns were those that appeared consistently across multiple platforms. Campaigns like Langston Party and March Book Madness performed well on Facebook, Instagram, and Email — suggesting that cross-channel promotion significantly boosts engagement."
    )

    st.subheader("Are there months or events with more engagement than others?")

    fb_df["publish_time"] = pd.to_datetime(fb_df["publish_time"], errors="coerce")
    fb_df["Month"] = fb_df["publish_time"].dt.to_period("M")
    fb_monthly = fb_df.groupby("Month")["total_engagement"].sum().reset_index()

    # Instagram
    meta_suite_df.columns = (
        meta_suite_df.columns.str.strip().str.lower().str.replace(" ", "_")
    )
    meta_suite_df["publish_time"] = pd.to_datetime(
        meta_suite_df["publish_time"], errors="coerce"
    )
    meta_suite_df["Month"] = meta_suite_df["publish_time"].dt.to_period("M")
    insta_monthly = (
        meta_suite_df.groupby("Month")[["likes", "comments", "shares"]]
        .sum()
        .sum(axis=1)
        .reset_index(name="total_engagement")
    )

    # LinkedIn
    activity_df["Month"] = activity_df["Date"].dt.to_period("M")
    linkedin_monthly = (
        activity_df.groupby("Month")["Total Engagement"].sum().reset_index()
    )

    # Combine into one DataFrame
    fb_monthly["Platform"] = "Facebook"
    insta_monthly["Platform"] = "Instagram"
    linkedin_monthly["Platform"] = "LinkedIn"

    fb_monthly.columns = ["Month", "Engagement", "Platform"]
    insta_monthly.columns = ["Month", "Engagement", "Platform"]
    linkedin_monthly.columns = ["Month", "Engagement", "Platform"]

    combined_monthly = pd.concat([fb_monthly, insta_monthly, linkedin_monthly])
    combined_monthly["Month"] = combined_monthly["Month"].astype(str)

    combined_monthly.head()

    # Aggregate engagement across platforms by month
    monthly_engagement = combined_monthly.groupby(
        ["Month", "Platform"], as_index=False
    ).agg({"Engagement": "sum"})

    combined_monthly_clean = combined_monthly.drop_duplicates(
        subset=["Month", "Platform"]
    )

    line_chart = (
        alt.Chart(combined_monthly_clean)
        .mark_line(point=True)
        .encode(
            x=alt.X("Month:T", title=None),
            y=alt.Y("Engagement:Q", title="Engagement"),
            color="Platform:N",
            tooltip=["Month:T", "Platform:N", "Engagement:Q"],
        )
        .interactive()
        .configure_view(stroke=None)
        .configure_axis(grid=False, domain=False, title=None)
        .properties(width=700, height=300)
    )
    st.altair_chart(line_chart, use_container_width=False)

    st.markdown(
        "Seasonal patterns show that January and March are strong periods for engagement, aligning with EOY fundraising and Book Madness. Planning major campaigns around these months—and mirroring themes across platforms—can significantly increase overall impact."
    )

    st.subheader("Summary")
    st.markdown(
        """
    - **Facebook**: Highest total reach (4,495) and engagement (302) across all platforms
    - **Instagram**: Best performance in profile visits (266) with fewer posts — strong conversion potential
    - **LinkedIn**: Moderate impressions and engagement; lowest return per post
    """
    )

    st.subheader("Recommendations")
    st.markdown(
        """
    1. **Use Instagram for High-Intent Engagement**: Post more Reels and direct followers to your profile link. Prioritize storytelling and action CTAs.
    2. **Double Down on Facebook for Awareness**: Use photo-based gratitude and event posts; optimize for shares and reactions.
    3. **Strengthen LinkedIn with Staff & Partner Content**: Post behind-the-scenes, event recaps, and team features. Boost post frequency.
    4. **Run Campaigns Cross-Platform, Timed to Seasons**: Coordinate messaging in January, March, and late fall.
    5. **Use Analytics to Repurpose Winning Content**: Turn high-performing Facebook posts into LinkedIn carousels and Email campaigns into Instagram infographics.
    """
    )
