import streamlit as st
import pandas as pd
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
import streamlit.components.v1 as components
import secrets
import json
from sqlalchemy import text


model = ChatOpenAI(
    openai_api_base=st.secrets["model_api"],
    openai_api_key=st.secrets["model_key"],
    model_name=st.secrets["model_name"],
)

st.set_page_config(page_title="Questionnaire", page_icon=":green_salad:")


if True:
    if "data_dict" not in st.session_state:
        st.session_state.data_dict = {
            "OpenAt": pd.Timestamp.now(),
            "GROUP_PERSONALIZED": secrets.choice([1, 2, 3, 4]),
        }
    if "page_num" not in st.session_state:
        st.session_state.page_num = 0
    if "chat_num" not in st.session_state:
        st.session_state.chat_num = 0
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "init_chat" not in st.session_state:
        st.session_state.init_chat = True
    if "chat_disabled" not in st.session_state:
        st.session_state.chat_disabled = False
    if "submitted" not in st.session_state:
        st.session_state.submitted = False
st.markdown(
    """
    <style>
        .reportview-container {
            margin-top: -2em;
        }
        #MainMenu {visibility: hidden;}
        .stAppDeployButton {display:none;}
        footer {visibility: hidden;}
        #stDecoration {display:none;}
        stSidebar {visibility: hidden;}
        div[data-testid="stMarkdownContainer"] {font-size: 16px;}
        # div[data-testid="stToolbar"] {visibility: hidden;}
        # div[data-testid="stSidebarContent"] {display: none;}
        # section[data-testid="stSidebar"] {display: none;}
        # div[data-testid="stSidebarCollapsedControl"] {display: none;}
        label[data-testid="stWidgetLabel"] {padding-left: 10px;border-left: 2px solid black;}
    </style>
""",
    unsafe_allow_html=True,
)


def transform_PB(x):
    pb_dict = {
        "Strongly Disagree": 1,  # 完全不同意
        "Disagree": 2,  # 不同意
        "Somewhat Disagree": 3,  # 有点不同意
        "Neither Agree nor Disagree": 4,  # 很难说同意或不同意
        "Somewhat Agree": 5,  # 有点同意
        "Agree": 6,  # 同意
        "Strongly Agree": 7,  # 完全同意
    }
    return pb_dict[x]


def goToNextPage_1():
    st.session_state.page_num = 1


def goToNextPage_2():
    st.session_state.page_num = 2


def goToNextPage_25():
    st.session_state.page_num = 2.5


def goToNextPage_3():
    st.session_state.page_num = 3


def goToNextPage_4():
    st.session_state.page_num = 4


def goToNextPage_45():
    st.session_state.page_num = 4.5


def goToNextPage_5():
    st.session_state.page_num = 5


def goToNextPage_6():
    st.session_state.page_num = 6


def goToNextPage_7():
    st.session_state.page_num = 7


def goToNextPage_8():
    st.session_state.page_num = 8


def goToNextPage_9():
    st.session_state.page_num = 9


def goToNextPage_95():
    st.session_state.page_num = 9.5


def goToNextPage_10():
    st.session_state.page_num = 10


def stream_response(response):
    for chunk in response:
        yield chunk.content


def response_decorator(func):
    def wrapper(messages):
        return stream_response(func(messages))

    return wrapper


@response_decorator
def get_response(messages):
    return model.stream(messages)


if st.session_state.page_num == 0:
    st.progress(0, text=":primary-badge[Your Progress]")  # 您的回答进度
    # st.write(st.session_state["data_dict"]["GROUP_PERSONALIZED"])
    st.title(
        "Survey on Public Attitudes and Perceptions toward Genetically Modified Foods"
    )  # 公众对转基因食品态度及观念调研
    st.header("Informed Consent Form")  # 知情同意书
    st.markdown(
        """

**Research Description**

Thank you for participating in this study. This study is jointly conducted by scholars from the School of Journalism and Communication at Beijing Normal University and the Department of Communication at the University of Zurich, Switzerland. Before starting, please carefully read the following information to ensure you understand the purpose and procedures of this study.

**Purpose of This Study**

The purpose of this study is to gain an in-depth understanding of public attitudes, perceptions, and behaviors toward genetically modified foods. This study can help us better understand how people view this type of new technology.

**Content of This Study**

If you choose to participate in this study, you will be asked to complete an online questionnaire, which will take approximately 15 minutes. Please answer based on your actual situation according to the instructions in the questionnaire. There are no standard answers to the questions, and they do not involve any value judgments.

**Compensation for This Study**

You will receive compensation after completing the questionnaire. If you withdraw midway or fail the attention check, you will not receive compensation.

**Anonymity and Security Protection**

This study does not involve any experiments related to human safety. We will also fully protect your privacy in research and publication. **We will not collect any information that can identify your identity**, and questionnaire data will be saved using randomly generated ID numbers. Research data published in any scientific journal or elsewhere will be anonymous and cannot be traced back to you. All data will only be used for academic research and will not be used for commercial or other non-research purposes. Researchers will take all controllable confidentiality precautions.

Your participation is entirely voluntary. You have the right to choose not to participate, and you may withdraw from this study at any time.
"""
    )
    st.radio(
        '**By selecting "I Agree to Participate", you agree to the above terms and conditions.**',  # 选择 「我同意参加」，即表示您同意上述条款和条件。
        [
            "I Agree to Participate",  # 我同意参加
            "I Do Not Agree to Participate",  # 我不同意参加
        ],
        key="CONSCENT",
        label_visibility="visible",
        index=None,
        horizontal=True,
    )
    agree = st.session_state.CONSCENT == "I Agree to Participate"
    # Display start button after agreement 同意后显示开始按钮
    if agree:
        participant_code = st.text_input(
            label="Please enter your participant code:"
        )  # 请输入您的被试编号：
        if participant_code:
            st.markdown(
                "Click the **Start** button to begin the survey"
            )  # 点击**开始**按钮进入调研
            st.session_state.data_dict["CONSCENT"] = agree
            st.session_state.data_dict["CODE"] = participant_code
            # When start button is clicked, increment page number 当开始按钮被点击，令页数 +1
            st.button("Start", on_click=goToNextPage_1)  # 开始
    else:
        st.session_state.data_dict["CONSCENT"] = agree

if st.session_state.page_num == 1:
    st.session_state.data_dict["StartAt"] = pd.Timestamp.now()
    st.progress(8, text=":primary-badge[Your Progress]")  # 您的回答进度
    st.markdown(
        "At the beginning of this survey, we would like to ask you some questions about yourself."
    )  # 在本次调查的开始，我们想问您一些关于您自己的信息。
    # Gender selection radio button 性别选择单选按钮
    gender = st.radio(
        "What gender do you identify as?",  # 您认为自己是什么性别？
        ["Male", "Female", "Other"],  # 男性，女性，其他
        key="DEM_GENDER",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        horizontal=True,
    )

    # If user selects "Other", display a text input 如果用户选择"其他"，显示一个输入框
    if gender == "Other":
        other_gender = st.text_input(
            "Please tell us your gender", key="DEM_GENDER_OTHER"
        )  # 请告诉我们您的性别
    else:
        # If user didn't select "Other", clear any existing input 如果用户没有选择"其他"，则清空可能存在的输入
        st.session_state.DEM_GENDER_OTHER = None
    age = st.number_input(
        label="What is your age?",
        min_value=0,
        max_value=120,
        key="DEM_AGE",  # 您的年龄多大？
    )
    residence = st.radio(
        "Where do you primarily live?",  # 您主要生活在？
        ["Urban Area", "Rural/Township Area"],  # 城市地区，乡镇地区
        key="DEM_RESID",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        horizontal=True,
    )
    education = st.radio(
        "What is your educational background?",  # 您的文化背景是？
        [
            "No Formal Education",
            "Elementary School",
            "Junior High School",
            "High School",
            "Undergraduate/Associate Degree",
            "Master's Degree",
            "Doctoral Degree",
        ],  # 没上过学，小学，初中，高中，本科或专科，硕士研究生，博士研究生
        key="DEM_EDU",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        horizontal=True,
    )
    income = st.number_input(
        "What is your approximate monthly disposable income (in yuan)?",
        min_value=0,
        key="DEM_INCOME",  # 您每月的可支配收入大约为多少元？
    )
    attcheck_1 = st.number_input(
        "Please enter the number 408 in the comment box.",
        min_value=0,
        key="ATTCHECK_1",  # 请将数字 408 写进评论框。
    )
    if gender and age and residence and education and attcheck_1:
        st.session_state.data_dict["DEM_GENDER"] = st.session_state.DEM_GENDER
        st.session_state.data_dict["DEM_GENDER_OTHER"] = (
            st.session_state.DEM_GENDER_OTHER
        )
        st.session_state.data_dict["DEM_AGE"] = st.session_state.DEM_AGE
        st.session_state.data_dict["DEM_RESID"] = st.session_state.DEM_RESID
        st.session_state.data_dict["DEM_EDU"] = st.session_state.DEM_EDU
        st.session_state.data_dict["DEM_INCOME"] = st.session_state.DEM_INCOME
        st.session_state.data_dict["ATTCHECK_1"] = st.session_state.ATTCHECK_1
        _, _, _, _, right = st.columns(5)
        with right:
            st.button("Next Page", on_click=goToNextPage_2)  # 下一页

if st.session_state.page_num == 2:
    st.progress(15, text=":primary-badge[Your Progress]")  # 您的回答进度
    st.markdown(
        "Please complete the following 6 **single-choice questions** based on your understanding of Artificial Intelligence (AI)."
    )  # 请根据您对人工智能（AI）的了解，完成以下6道**单选题**。
    AI_USE_1 = st.selectbox(
        "I can operate AI applications in my daily life.",  # 我可以在日常生活中操作AI应用。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="AI_USE_1",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    AI_USE_2 = st.selectbox(
        "I can use AI applications to make my daily life easier.",  # 我可以使用AI应用来使我的日常生活更加轻松。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="AI_USE_2",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    AI_USE_3 = st.selectbox(
        "I can use AI purposefully to achieve my daily goals.",  # 我可以有目的地使用AI来实现我的日常目标。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="AI_USE_3",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    AI_USE_4 = st.selectbox(
        "In daily life, I can interact with AI in a way that makes my tasks easier.",  # 在日常生活中，我可以用一种使我的任务更轻松的方式与AI互动。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="AI_USE_4",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    AI_USE_5 = st.selectbox(
        "In daily life, I can benefit from collaborating with AI.",  # 在日常生活中，我可以通过与AI合作获得好处。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="AI_USE_5",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    AI_USE_6 = st.selectbox(
        "I can communicate effectively with AI in daily life.",  # 我可以在日常生活中与AI进行有益的沟通。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="AI_USE_6",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    if AI_USE_1 and AI_USE_2 and AI_USE_3 and AI_USE_4 and AI_USE_5 and AI_USE_6:
        st.session_state.data_dict["AI_USE_1"] = st.session_state.AI_USE_1
        st.session_state.data_dict["AI_USE_2"] = st.session_state.AI_USE_2
        st.session_state.data_dict["AI_USE_3"] = st.session_state.AI_USE_3
        st.session_state.data_dict["AI_USE_4"] = st.session_state.AI_USE_4
        st.session_state.data_dict["AI_USE_5"] = st.session_state.AI_USE_5
        st.session_state.data_dict["AI_USE_6"] = st.session_state.AI_USE_6
        _, _, _, _, right = st.columns(5)
        with right:
            st.button("Next Page", on_click=goToNextPage_25)  # 下一页
if st.session_state.page_num == 2.5:
    st.progress(23, text=":primary-badge[Your Progress]")  # 您的回答进度
    st.markdown(
        "Please complete the following 6 **single-choice questions** based on your understanding of Artificial Intelligence (AI)."
    )  # 请根据您对人工智能（AI）的了解，完成以下6道**单选题**。
    AI_KNOW_1 = st.selectbox(
        "I understand the most important concepts of AI.",  # 我了解AI这一主题的最重要概念。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="AI_KNOW_1",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    AI_KNOW_2 = st.selectbox(
        "I know the definition of AI.",  # 我知道AI的定义。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="AI_KNOW_2",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    AI_KNOW_3 = st.selectbox(
        "I can evaluate the limitations and opportunities of using AI.",  # 我可以评估使用AI的限制和机会。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="AI_KNOW_3",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    AI_KNOW_4 = st.selectbox(
        "I can evaluate the advantages and disadvantages of using AI.",  # 我可以评估使用AI所带来的优势和劣势。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="AI_KNOW_4",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    AI_KNOW_5 = st.selectbox(
        "I can think of new uses for AI.",  # 我可以思考AI的新用途。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="AI_KNOW_5",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    AI_KNOW_6 = st.selectbox(
        "I can imagine possible future applications of AI.",  # 我可以想象AI可能的未来应用。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="AI_KNOW_6",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    if AI_KNOW_1 and AI_KNOW_2 and AI_KNOW_3 and AI_KNOW_4 and AI_KNOW_5 and AI_KNOW_6:
        st.session_state.data_dict["AI_KNOW_1"] = st.session_state.AI_KNOW_1
        st.session_state.data_dict["AI_KNOW_2"] = st.session_state.AI_KNOW_2
        st.session_state.data_dict["AI_KNOW_3"] = st.session_state.AI_KNOW_3
        st.session_state.data_dict["AI_KNOW_4"] = st.session_state.AI_KNOW_4
        st.session_state.data_dict["AI_KNOW_5"] = st.session_state.AI_KNOW_5
        st.session_state.data_dict["AI_KNOW_6"] = st.session_state.AI_KNOW_6
        _, _, _, _, right = st.columns(5)
        with right:
            st.button("Next Page", on_click=goToNextPage_3)  # 下一页
if st.session_state.page_num == 3:
    st.progress(30, text=":primary-badge[Your Progress]")  # 您的回答进度
    st.markdown(
        "We would like to know your views on scientists in our country, including those working in universities, government, companies, and non-profit organizations."  # 我们想知道您对本国科学家的看法，包括在大学、政府、公司和非营利组织工作的科学家。
    )
    TRUST_SCI_honest = st.selectbox(
        "How honest or dishonest are most scientists?",  # 大多数科学家的诚实或不诚实程度如何？
        [
            "Very Dishonest",  # 非常不诚实
            "Dishonest",  # 不诚实
            "Somewhat Dishonest",  # 有点不诚实
            "Neither Honest nor Dishonest",  # 谈不上诚实，也不算不诚实
            "Somewhat Honest",  # 有点诚实
            "Honest",  # 诚实
            "Very Honest",  # 非常诚实
        ],
        key="TRUST_SCI_honest",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    TRUST_SCI_concerned = st.selectbox(
        "How concerned or unconcerned are most scientists about people's well-being?",  # 大多数科学家对人们的福祉有多关注或不关注？
        [
            "Very Unconcerned",  # 非常不关心
            "Unconcerned",  # 不关心
            "Somewhat Unconcerned",  # 有点不关心
            "Neither Concerned nor Unconcerned",  # 谈不上关心，也不算不关心
            "Somewhat Concerned",  # 有点关心
            "Concerned",  # 关心
            "Very Concerned",  # 非常关心
        ],
        key="TRUST_SCI_concerned",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    TRUST_SCI_ethical = st.selectbox(
        "What do you think is the moral standard of most scientists?",  # 你觉得大多数科学家的道德水平如何？
        [
            "Very Low",  # 非常低
            "Low",  # 低
            "Somewhat Low",  # 比较低
            "Neither High nor Low",  # 算不上高，也算不上低
            "Somewhat High",  # 比较高
            "High",  # 高
            "Very High",  # 非常高
        ],
        key="TRUST_SCI_ethical",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    TRUST_SCI_improve = st.selectbox(
        "How enthusiastic are most scientists about improving other people's lives?",  # 你觉得大多数科学家改善他人生活的热心程度如何？
        [
            "Very Indifferent",  # 非常冷漠
            "Indifferent",  # 冷漠
            "Somewhat Indifferent",  # 比较冷漠
            "Neither Enthusiastic nor Indifferent",  # 算不上热心，也算不上冷漠
            "Somewhat Enthusiastic",  # 比较热心
            "Enthusiastic",  # 热心
            "Very Enthusiastic",  # 非常热心
        ],
        key="TRUST_SCI_improve",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    TRUST_SCI_sincere = st.selectbox(
        "Do you think most scientists are sincere?",  # 你觉得大多数科学家是否真诚?
        [
            "Very Insincere",  # 非常不真诚
            "Insincere",  # 不真诚
            "Somewhat Insincere",  # 比较不真诚
            "Neither Sincere nor Insincere",  # 算不上真诚，也算不上不真诚
            "Somewhat Sincere",  # 比较真诚
            "Sincere",  # 真诚
            "Very Sincere",  # 非常真诚
        ],
        key="TRUST_SCI_sincere",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    TRUST_SCI_otherint = st.selectbox(
        "How much do you think most scientists care about the interests of others?",  # 你认为大多数科学家对他人的利益有多在意？
        [
            "Very Uncaring",  # 非常不在意
            "Uncaring",  # 不在意
            "Somewhat Uncaring",  # 比较不在意
            "Neither Caring nor Uncaring",  # 算不上在意，也算不上不在意
            "Somewhat Caring",  # 比较在意
            "Caring",  # 在意
            "Very Caring",  # 非常在意
        ],
        key="TRUST_SCI_otherint",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    if (
        TRUST_SCI_honest
        and TRUST_SCI_concerned
        and TRUST_SCI_ethical
        and TRUST_SCI_improve
        and TRUST_SCI_sincere
        and TRUST_SCI_otherint
    ):
        st.session_state.data_dict["TRUST_SCI_honest"] = (
            st.session_state.TRUST_SCI_honest
        )
        st.session_state.data_dict["TRUST_SCI_concerned"] = (
            st.session_state.TRUST_SCI_concerned
        )
        st.session_state.data_dict["TRUST_SCI_ethical"] = (
            st.session_state.TRUST_SCI_ethical
        )
        st.session_state.data_dict["TRUST_SCI_improve"] = (
            st.session_state.TRUST_SCI_improve
        )
        st.session_state.data_dict["TRUST_SCI_sincere"] = (
            st.session_state.TRUST_SCI_sincere
        )
        st.session_state.data_dict["TRUST_SCI_otherint"] = (
            st.session_state.TRUST_SCI_otherint
        )
        _, _, _, _, right = st.columns(5)
        with right:
            st.button("Next Page", on_click=goToNextPage_4)  # 下一页
if st.session_state.page_num == 4:
    st.progress(38, text=":primary-badge[Your Progress]")  # 您的回答进度
    st.markdown(
        "Next, we would like to understand your attitude toward genetically modified foods."
    )  # 接下来，我们想了解您对转基因食品的态度。

    PRE_ATTITUDE_health = st.selectbox(
        "Genetically modified foods are safe for human consumption.",  # 转基因食品对人体是安全的。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="PRE_ATTITUDE_health",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    PRE_ATTITUDE_econ = st.selectbox(
        "Genetically modified foods have economic utility value.",  # 转基因食品具有经济上的利用价值。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="PRE_ATTITUDE_econ",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    PRE_ATTITUDE_env = st.selectbox(
        "Genetically modified foods do not cause environmental damage.",  # 转基因食品不会造成环境破坏。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="PRE_ATTITUDE_env",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    PRE_ATTITUDE_ethic = st.selectbox(
        "I can accept genetically modified foods ethically.",  # 我在伦理道德上可以接受转基因食品。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="PRE_ATTITUDE_ethic",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    if (
        PRE_ATTITUDE_health
        and PRE_ATTITUDE_econ
        and PRE_ATTITUDE_env
        and PRE_ATTITUDE_ethic
    ):
        st.session_state.data_dict["PRE_ATTITUDE_health"] = (
            st.session_state.PRE_ATTITUDE_health
        )
        st.session_state.data_dict["PRE_ATTITUDE_econ"] = (
            st.session_state.PRE_ATTITUDE_econ
        )
        st.session_state.data_dict["PRE_ATTITUDE_env"] = (
            st.session_state.PRE_ATTITUDE_env
        )
        st.session_state.data_dict["PRE_ATTITUDE_ethic"] = (
            st.session_state.PRE_ATTITUDE_ethic
        )
        _, _, _, _, right = st.columns(5)
        with right:
            st.button("Next Page", on_click=goToNextPage_45)  # 下一页
if st.session_state.page_num == 4.5:
    st.progress(45, text=":primary-badge[Your Progress]")  # 您的回答进度
    st.markdown(
        "We would like to continue to understand your attitude toward genetically modified foods."
    )  # 我们想继续了解您对转基因食品的态度。

    PRE_WILLING_BUY = st.selectbox(
        "I am willing to purchase genetically modified foods.",  # 我愿意购买转基因食品。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="PRE_WILLING_BUY",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    PRE_WILLING_EAT = st.selectbox(
        "I am willing to consume genetically modified foods.",  # 我愿意食用转基因食品。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="PRE_WILLING_EAT",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    PRE_WILLING_SHARE = st.selectbox(
        "I am willing to share genetically modified foods with others.",  # 我愿意分享转基因食品给他人。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="PRE_WILLING_SHARE",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    if PRE_WILLING_BUY and PRE_WILLING_EAT and PRE_WILLING_SHARE:

        st.session_state.data_dict["PRE_WILLING_BUY"] = st.session_state.PRE_WILLING_BUY
        st.session_state.data_dict["PRE_WILLING_EAT"] = st.session_state.PRE_WILLING_EAT
        st.session_state.data_dict["PRE_WILLING_SHARE"] = (
            st.session_state.PRE_WILLING_SHARE
        )
        _, _, _, _, right = st.columns(5)
        with right:
            st.button("Next Page", on_click=goToNextPage_5)  # 下一页
    # st.write(st.session_state.data_dict)
if st.session_state.page_num == 5:
    st.progress(53, text=":primary-badge[Your Progress]")  # 您的回答进度
    st.markdown(
        "Next, we would like to understand some of your specific views on genetically modified foods."
    )  # 接下来，我们想了解您对转基因食品的一些具体看法。
    PRE_BELIEF_1 = st.selectbox(
        "I am concerned about the impact of genetically modified foods on consumer health.",  # 我对转基因食品对消费者健康的影响感到担忧。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="PRE_BELIEF_1",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    PRE_BELIEF_2 = st.selectbox(
        "Genetically modified foods may pose risks to human health.",  # 转基因食品可能对人类健康构成风险。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="PRE_BELIEF_2",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    PRE_BELIEF_3 = st.selectbox(
        "Genetically modified foods may cause human diseases.",  # 转基因食品可能引发人类疾病。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="PRE_BELIEF_3",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    PRE_BELIEF_4 = st.selectbox(
        "Widespread cultivation of genetically modified crops may have a negative impact on biodiversity in nature.",  # 转基因作物的广泛种植可能会对自然界的生物多样性产生负面影响。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="PRE_BELIEF_4",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    PRE_BELIEF_5 = st.selectbox(
        "Consuming genetically modified foods may lead to the transfer of artificially edited genetic material into the human body.",  # 摄入转基因食品可能导致人工编辑的遗传物质转移到人体内。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="PRE_BELIEF_5",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    if PRE_BELIEF_1 and PRE_BELIEF_2 and PRE_BELIEF_3 and PRE_BELIEF_4 and PRE_BELIEF_5:
        st.session_state.data_dict["PRE_BELIEF_1"] = transform_PB(
            st.session_state.PRE_BELIEF_1
        )
        st.session_state.data_dict["PRE_BELIEF_2"] = transform_PB(
            st.session_state.PRE_BELIEF_2
        )
        st.session_state.data_dict["PRE_BELIEF_3"] = transform_PB(
            st.session_state.PRE_BELIEF_3
        )
        st.session_state.data_dict["PRE_BELIEF_4"] = transform_PB(
            st.session_state.PRE_BELIEF_4
        )
        st.session_state.data_dict["PRE_BELIEF_5"] = transform_PB(
            st.session_state.PRE_BELIEF_5
        )
        st.session_state.data_dict["PRE_BELIEF"] = (
            st.session_state.data_dict["PRE_BELIEF_1"]
            + st.session_state.data_dict["PRE_BELIEF_2"]
            + st.session_state.data_dict["PRE_BELIEF_3"]
            + st.session_state.data_dict["PRE_BELIEF_4"]
            + st.session_state.data_dict["PRE_BELIEF_5"]
        ) / 5
        _, _, _, _, right = st.columns(5)
        with right:
            st.button("Next Page", on_click=goToNextPage_6)  # 下一页
if st.session_state.page_num == 6:
    st.progress(60, text=":primary-badge[Your Progress]")  # 您的回答进度
    st.markdown(
        """
Next, you will have a conversation with an AI assistant on a topic related to genetically modified foods.

1. First, please describe in 20-100 words what you are most concerned about in the field of genetically modified foods.
2. After proceeding to the next page, please discuss your concerns with the AI.
"""  # 接下来，您将就一个与转基因食品相关的主题与AI助手对话。
        # 1. 首先请您用20至100字具体阐述您在转基因食品领域最感兴趣的关注点。
        # 2. 跳转下页后，请您与AI讨论您的关注议题。
    )
    st.markdown(
        """
The following topics are the areas of greatest concern when people discuss genetically modified foods. You may use them as a reference.

+ Safety Risks
  For example, is it safe for me?
+ Environmental Impact
  For example, does it have an impact on the environment?
+ Economic Value
  For example, can it reduce my cost of living?
+ Ethics
  For example, is modifying genes ethical?

"""  # 以下议题是人们在讨论转基因食品时最常关心的几个领域。您可以将其作为参考。
        # + 安全风险 例如，对我来说安全吗？
        # + 环境影响 例如，对环境是否有影响？
        # + 经济价值 例如，能降低我的生活成本吗？
        # + 伦理道德 例如，修改生物基因是否道德？
    )

    CONCERN_DETAIL = st.text_area(
        label="Regarding genetically modified foods, can you specifically talk about your concerns?",  # 在转基因食品上，您可以具体讲讲您的关注点吗？
        placeholder="Please enter approximately 20-100 characters.",  # 请输入大约20-100字。
        key="CONCERN_DETAIL",
        max_chars=100,
    )
    instruction = (
        "Please write more to help us better understand your viewpoint."  # 再多写一些可以帮助我们更好地了解您的观点~
        if len(CONCERN_DETAIL) < 20
        else 'You can click "Next Page" to continue.'  # 可以点击"下一页"继续作答了~
    )
    st.write(
        f"You have entered {len(CONCERN_DETAIL)} characters. {instruction}"
    )  # 您已输入X字。
    if len(CONCERN_DETAIL) >= 20:
        # st.session_state.data_dict["TOPIC"] = st.session_state.TOPIC
        st.session_state.data_dict["CONCERN_DETAIL"] = st.session_state.CONCERN_DETAIL
        _, _, _, _, right = st.columns(5)
        with right:
            st.button("Next Page", on_click=goToNextPage_7)  # 下一页
if st.session_state.page_num == 7:
    st.progress(67, text=":primary-badge[Your Progress]")  # 您的回答进度
    st.write(
        "Next, you will have **up to five** opportunities to converse with the AI. Please discuss your selected topic with the AI."  # 接下来，您将获得**至多五次**与AI对话的机会。请您围绕您刚刚选择的主题与AI进行交流。
    )
    st.write(
        "After the first round of conversation, you only need to have **one more conversation** to proceed to the next round."
    )  # 在第一轮对话后，您只需**再进行一次对话**就可以进入下一轮

    tip = ":blue-badge[This AI's responses have been reviewed by experts in the field of genetically modified foods. Please carefully evaluate the information.]"  # 本 AI 的回答经过了转基因食品领域专家的检查，请仔细甄别。
    st.markdown(tip)
    user_input = st.chat_input(
        f"You have {5-st.session_state.chat_num} conversation opportunities remaining. Please enter...",  # 您还有X次对话机会，请输入...
        disabled=st.session_state.chat_disabled,
    )
    # Display chat history 显示聊天历史
    for message in st.session_state.messages:
        if message["role"] == "system":
            continue
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            if message["role"] == "assistant":
                st.markdown(tip)

    if st.session_state.init_chat:
        st.session_state.init_chat = False
        with st.chat_message("user"):
            init_input = f"Hello, I would like to learn about genetically modified foods. My specific question is: {st.session_state.data_dict['CONCERN_DETAIL']}"  # 你好，我想要了解转基因食品。我的具体问题是：X
            st.markdown(init_input)
        personalized = st.session_state.data_dict["GROUP_PERSONALIZED"]
        if personalized == 1:
            # Control Group 对照组
            st.session_state.messages.append(
                {
                    "role": "system",
                    "content": "You are an expert in the field of genetically modified foods. Please answer user-related questions in 150-200 words.",  # 你是一位转基因食品领域的专家，请用150-200词回答用户的相关问题。
                }
            )
        elif personalized == 2:
            # Demo Group 人口学组
            personalized_profile = f'The user you will face is a {st.session_state.data_dict["DEM_AGE"]}-year-old {st.session_state.data_dict["DEM_GENDER_OTHER"] if st.session_state.data_dict["DEM_GENDER_OTHER"] else st.session_state.data_dict["DEM_GENDER"]} living in {st.session_state.data_dict["DEM_RESID"]}. Their education level is {st.session_state.data_dict["DEM_EDU"]}, and their monthly disposable income is approximately {st.session_state.data_dict["DEM_INCOME"]} yuan. **Do not reveal user information.**'  # 你将面对的用户是一位居住在X的Y岁Z，ta的教育程度是W，ta的每月可支配收入约为V元。**不要透露用户信息。**
            st.session_state.messages.append(
                {
                    "role": "system",
                    "content": "You are an expert in the field of genetically modified foods. Please answer user-related questions in 150-200 words. "  # 你是一位转基因食品领域的专家，请用150-200词回答用户的相关问题。
                    + personalized_profile,
                }
            )
        elif personalized == 3:
            # PB Group 信念组
            if st.session_state.data_dict["PRE_BELIEF"] > 4:
                personalized_profile = "The user you will face has relatively deep misconceptions about genetically modified foods. Please carefully consider your wording when communicating with them. When interacting with them, you may consider using conformity psychology or introducing the benefits of genetically modified foods to demonstrate their value."  # 你将要面对的用户对转基因食品存在较深刻的误解。请你谨慎考虑与其交流时的用词。在与ta交流时，你可以考虑利用从众心理，也可以介绍转基因食品的好处向ta展示转基因食品的价值。
            else:
                personalized_profile = "The user you will face has a relatively optimistic view of genetically modified foods. You can cite opinions or suggestions from authoritative figures or institutions to enhance persuasiveness, and you can introduce more benefits of genetically modified foods to them."  # 你将要面对的用户对转基因食品的观点是相对乐观的。你可以引用权威人士或机构的观点或建议以增强劝服力，你可以为ta介绍转基因食品的更多好处。
            st.session_state.messages.append(
                {
                    "role": "system",
                    "content": "You are an expert in the field of genetically modified foods. Please answer user-related questions in 150-200 words. "  # 你是一位转基因食品领域的专家，请用150-200词回答用户的相关问题。
                    + personalized_profile,
                }
            )
        elif personalized == 4:
            # Demo + PB 人口学+信念组
            personalized_profile = f'The user you will face is a {st.session_state.data_dict["DEM_AGE"]}-year-old {st.session_state.data_dict["DEM_GENDER_OTHER"] if st.session_state.data_dict["DEM_GENDER_OTHER"] else st.session_state.data_dict["DEM_GENDER"]} living in {st.session_state.data_dict["DEM_RESID"]}. Their education level is {st.session_state.data_dict["DEM_EDU"]}, and their monthly disposable income is approximately {st.session_state.data_dict["DEM_INCOME"]} yuan. **Do not reveal user information.**'  # 你将面对的用户是一位居住在X的Y岁Z，ta的教育程度是W，ta的每月可支配收入约为V元。**不要透露用户信息。**
            if st.session_state.data_dict["PRE_BELIEF"] > 4:
                personalized_profile += "The user you will face has relatively deep misconceptions about genetically modified foods. Please carefully consider your wording when communicating with them. When interacting with them, you may consider using conformity psychology or introducing the benefits of genetically modified foods to demonstrate their value."  # 你将要面对的用户对转基因食品存在较深刻的误解。请你谨慎考虑与其交流时的用词。在与ta交流时，你可以考虑利用从众心理，也可以介绍转基因食品的好处向ta展示转基因食品的价值。
            else:
                personalized_profile += "The user you will face has a relatively optimistic view of genetically modified foods. You can cite opinions or suggestions from authoritative figures or institutions to enhance persuasiveness, and you can introduce more benefits of genetically modified foods to them."  # 你将要面对的用户对转基因食品的观点是相对乐观的。你可以引用权威人士或机构的观点或建议以增强劝服力，你可以为ta介绍转基因食品的更多好处。
            st.session_state.messages.append(
                {
                    "role": "system",
                    "content": "You are an expert in the field of genetically modified foods. Please answer user-related questions in 150-200 words. "  # 你是一位转基因食品领域的专家，请用150-200词回答用户的相关问题。
                    + personalized_profile,
                }
            )
        st.session_state.messages.append({"role": "user", "content": init_input})
        with st.chat_message("assistant"):
            response = st.write_stream(get_response(st.session_state.messages))
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    if user_input:
        st.session_state.chat_num += 1
        if st.session_state.chat_num >= 5:
            st.session_state.chat_disabled = True
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("assistant"):
            response = st.write_stream(get_response(st.session_state.messages))
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()
    _, _, _, _, right = st.columns(5)
    with right:
        if st.session_state.chat_num >= 1:
            st.button("Next Page", on_click=goToNextPage_8)  # 下一页

if st.session_state.page_num == 8:
    st.progress(75, text=":primary-badge[Your Progress]")  # 您的回答进度
    st.markdown(
        "The questionnaire is almost complete. We would like to ask you a few more questions."
    )  # 问卷马上就要结束了，我们还想再问您几个问题。
    st.markdown(
        "Please indicate your level of agreement with the following statements:"
    )  # 请对以下陈述表明您的同意程度：
    POST_sat_1 = st.selectbox(
        "I am very satisfied with the interaction with the AI.",  # 我对与AI的互动非常满意。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="POST_sat_1",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    POST_sat_2 = st.selectbox(
        "I was able to understand the interaction with the AI.",  # 我能够理解与AI的互动。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="POST_sat_2",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )

    POST_learning_1 = st.selectbox(
        "The AI helped me learn about genetically modified foods more quickly.",  # AI帮助我更快地了解转基因食品。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="POST_learning_1",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    POST_learning_2 = st.selectbox(
        "After conversing with the AI, I am more confident in my knowledge of genetically modified foods.",  # 与AI对话后，我对自己的转基因食品认知程度更有信心了。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="POST_learning_2",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    POST_continue = st.selectbox(
        "If possible, I would like to continue conversing with the AI.",  # 如果可以，我愿意继续与AI对话。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="POST_continue",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    POST_credibility_1 = st.selectbox(
        "The information I saw in this survey is credible.",  # 我在本调研中看到的信息是可信的。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="POST_credibility_1",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    POST_credibility_2 = st.selectbox(
        "The information I saw in this survey is accurate.",  # 我在本调研中看到的信息是准确的。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="POST_credibility_2",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    if (
        POST_sat_1
        and POST_sat_2
        and POST_learning_1
        and POST_learning_2
        and POST_continue
        and POST_credibility_1
        and POST_credibility_2
    ):
        st.session_state.data_dict["POST_sat_1"] = st.session_state.POST_sat_1
        st.session_state.data_dict["POST_sat_2"] = st.session_state.POST_sat_2
        st.session_state.data_dict["POST_learning_1"] = st.session_state.POST_learning_1
        st.session_state.data_dict["POST_learning_2"] = st.session_state.POST_learning_2
        st.session_state.data_dict["POST_continue"] = st.session_state.POST_continue
        st.session_state.data_dict["POST_credibility_1"] = (
            st.session_state.POST_credibility_1
        )
        st.session_state.data_dict["POST_credibility_2"] = (
            st.session_state.POST_credibility_2
        )
        _, _, _, _, right = st.columns(5)
        with right:
            st.button("Next Page", on_click=goToNextPage_9)  # 下一页
if st.session_state.page_num == 9:
    st.progress(83, text=":primary-badge[Your Progress]")  # 您的回答进度
    st.markdown(
        "We would like to ask you again about your attitude toward genetically modified foods."
    )  # 我们还想再次询问您对转基因食品的态度。
    POST_ATTITUDE_health = st.selectbox(
        "Genetically modified foods are safe for human consumption.",  # 转基因食品对人体是安全的。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="POST_ATTITUDE_health",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    POST_ATTITUDE_econ = st.selectbox(
        "Genetically modified foods have economic utility value.",  # 转基因食品具有经济上的利用价值。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="POST_ATTITUDE_econ",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    POST_ATTITUDE_env = st.selectbox(
        "Genetically modified foods do not cause environmental damage.",  # 转基因食品不会造成环境破坏。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="POST_ATTITUDE_env",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    POST_ATTITUDE_ethic = st.selectbox(
        "I can accept genetically modified foods ethically.",  # 我在伦理道德上可以接受转基因食品。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="POST_ATTITUDE_ethic",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    if (
        POST_ATTITUDE_health
        and POST_ATTITUDE_econ
        and POST_ATTITUDE_env
        and POST_ATTITUDE_ethic
    ):
        st.session_state.data_dict["POST_ATTITUDE_health"] = (
            st.session_state.POST_ATTITUDE_health
        )
        st.session_state.data_dict["POST_ATTITUDE_econ"] = (
            st.session_state.POST_ATTITUDE_econ
        )
        st.session_state.data_dict["POST_ATTITUDE_env"] = (
            st.session_state.POST_ATTITUDE_env
        )
        st.session_state.data_dict["POST_ATTITUDE_ethic"] = (
            st.session_state.POST_ATTITUDE_ethic
        )
        _, _, _, _, right = st.columns(5)
        with right:
            st.button("Next Page", on_click=goToNextPage_95)  # 下一页
if st.session_state.page_num == 9.5:
    st.progress(90, text=":primary-badge[Your Progress]")  # 您的回答进度
    st.markdown(
        "This is the final page of questions. Please hang in there!"
    )  # 本页是最后的题目，请您再坚持一下~

    ATTCHECK_2 = st.selectbox(
        'For this question, please select "Somewhat Agree".',  # 本题请选择有点同意。
        [
            "Strongly Disagree",  # 完全不同意
            "Disagree",  # 不同意
            "Somewhat Disagree",  # 有点不同意
            "Neither Agree nor Disagree",  # 很难说同意或不同意
            "Somewhat Agree",  # 有点同意
            "Agree",  # 同意
            "Strongly Agree",  # 完全同意
        ],
        key="ATTCHECK_2",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    POST_WILLING_BUY = st.selectbox(
        "Are you willing to purchase genetically modified foods?",  # 您愿意购买转基因食品吗？
        [
            "Strongly Unwilling",  # 完全不愿意
            "Unwilling",  # 不愿意
            "Somewhat Unwilling",  # 有点不愿意
            "Neither Willing nor Unwilling",  # 很难说愿意或不愿意
            "Somewhat Willing",  # 有点愿意
            "Willing",  # 愿意
            "Strongly Willing",  # 完全愿意
        ],
        key="POST_WILLING_BUY",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    POST_WILLING_EAT = st.selectbox(
        "Are you willing to consume genetically modified foods?",  # 您愿意食用转基因食品吗？
        [
            "Strongly Unwilling",  # 完全不愿意
            "Unwilling",  # 不愿意
            "Somewhat Unwilling",  # 有点不愿意
            "Neither Willing nor Unwilling",  # 很难说愿意或不愿意
            "Somewhat Willing",  # 有点愿意
            "Willing",  # 愿意
            "Strongly Willing",  # 完全愿意
        ],
        key="POST_WILLING_EAT",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )
    POST_WILLING_SHARE = st.selectbox(
        "Are you willing to share genetically modified foods with others?",  # 您愿意分享转基因食品给他人吗？
        [
            "Strongly Unwilling",  # 完全不愿意
            "Unwilling",  # 不愿意
            "Somewhat Unwilling",  # 有点不愿意
            "Neither Willing nor Unwilling",  # 很难说愿意或不愿意
            "Somewhat Willing",  # 有点愿意
            "Willing",  # 愿意
            "Strongly Willing",  # 完全愿意
        ],
        key="POST_WILLING_SHARE",
        label_visibility="visible",
        index=None,  # 默认不选中任何选项
        placeholder="Please select...",  # 请选择...
    )

    if ATTCHECK_2 and POST_WILLING_BUY and POST_WILLING_EAT and POST_WILLING_SHARE:

        st.session_state.data_dict["ATTCHECK_2"] = st.session_state.ATTCHECK_2
        st.session_state.data_dict["POST_WILLING_BUY"] = (
            st.session_state.POST_WILLING_BUY
        )
        st.session_state.data_dict["POST_WILLING_EAT"] = (
            st.session_state.POST_WILLING_EAT
        )
        st.session_state.data_dict["POST_WILLING_SHARE"] = (
            st.session_state.POST_WILLING_SHARE
        )
        _, _, _, _, right = st.columns(5)
        with right:
            st.button("Next Page", on_click=goToNextPage_10)  # 下一页


def on_submit():
    st.session_state.submitted = True
    data_dict = st.session_state.data_dict
    data_dict["chat_messages"] = json.dumps(
        st.session_state.messages
    )  # Ensure conversion to JSON string 确保转换为JSON字符串
    data_dict["chat_num"] = st.session_state.chat_num


#     try:
#         with conn.session as s:
#             s.execute(
#                 text(
#                     # Here is SQL insert instruction, e.g. 这里是 SQL 插入指令，例如
#                     """
# INSERT INTO test
# (
# a, b,c
# )
# VALUES (
# :a, :b, :c
# )
#             """
#                 ),
#                 data_dict,
#             )
#             s.commit()
#     except Exception as e:
#         st.error(f"Submission failed. Please contact...")  # 提交失败，请联系...
#         st.stop()


if st.session_state.page_num == 10:
    st.progress(100, text=":primary-badge[Your Progress]")  # 您的回答进度
    conn = st.connection("postgresql", type="sql")
    st.markdown(
        """Thank you for completing this questionnaire. Please:
1. Click the \"Submit\" button.
2. Wait for the prompt to exit the system."""  # 感谢您完成了本问卷，请您接下来：1. 点击「提交」按钮。2. 等待提示退出系统。
    )
    SUBMIT = st.button(
        "Submit",  # 提交
        disabled=st.session_state.submitted,  # 如果已提交则禁用按钮
        key="submit_button",
        on_click=on_submit,
    )
    if SUBMIT:
        st.write("Submitting... Please wait.")  # 正在提交...请稍候。
    if st.session_state.submitted:
        st.write(
            "Submission complete! You can exit this page."
        )  # 提交完成！您可以退出本页面。
        st.write(st.session_state.data_dict)
