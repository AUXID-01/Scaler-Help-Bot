import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from fuzzywuzzy import fuzz

load_dotenv()
TOKEN = os.getenv('TOKEN', '').strip()

qa_pairs = [
    {"question":"Hello","answer" : "Hi! Ask me any question related to SST admissions."},
    {"question" :"Hi","answer" : "Hi! Ask me any question related to SST admissions."},
    {"question": "Whom can I speak to know more about the program?", "answer": "We're delighted that you're interested in learning more about our program! To provide you with the best possible insight, we encourage you to attend our frequent live online admissions seminars. These sessions are hosted by the leadership team of the Scaler School of Technology (SST) and offer a fantastic opportunity for you to interact directly with our experts. You can ask any questions you have and gain a deeper understanding of what our program has to offer. Please visit Scaler School of Technology- https://www.scaler.com/school-of-technology/events Events to find out more about these seminars and how you can participate. In the meantime, we invite you to explore the wealth of information available on our website. You can also delve into our comprehensive video content on the SST YouTube page, which provides further insights into our program. For English speakers, we recommend this specific YouTube Playlist - https://youtube.com/playlist?list=PL_aMuHABgX0gwfsAsn10_glcHPPVkj5GF&si=WejVRjmYoAxHGSkY , which addresses important questions about the program. For Hindi speakers, this Hindi Playlist - https://youtube.com/playlist?list=PL_aMuHABgX0iUJ11svagyHeAmPvOfpo0m&si=bZcPgkE_ZvUZWCks is tailored to provide relevant information in Hindi. Apart from this you can reach out to our alumni network. We are proud to have alumni working at some of the top tech companies in the world. They are a valuable resource for understanding their experiences and reviewing our program. You can connect with them and learn more about their journey with Scaler by visiting our alumni review page at: https://www.scaler.com/review/ For those who have enrolled for the Scaler NSET exam, we offer dedicated support. You will receive an email ID and a support number to assist with any queries or issues you may face before or during the exam. Please note that detailed counselling sessions, involving both parents and students, are exclusively conducted for candidates who successfully clear the test and interviews. Once you receive an offer, your assigned admissions counsellor will reach out to you for further guidance and support."},
    {"question": "Can I get a contact number for a real person I can talk to?", "answer": "We're delighted that you're interested in learning more about our program! To provide you with the best possible insight, we encourage you to attend our frequent live online admissions seminars. These sessions are hosted by the leadership team of the Scaler School of Technology (SST) and offer a fantastic opportunity for you to interact directly with our experts. You can ask any questions you have and gain a deeper understanding of what our program has to offer. Please visit Scaler School of Technology- https://www.scaler.com/school-of-technology/events Events to find out more about these seminars and how you can participate. In the meantime, we invite you to explore the wealth of information available on our website. You can also delve into our comprehensive video content on the SST YouTube page, which provides further insights into our program. For English speakers, we recommend this specific YouTube Playlist - https://youtube.com/playlist?list=PL_aMuHABgX0gwfsAsn10_glcHPPVkj5GF&si=WejVRjmYoAxHGSkY , which addresses important questions about the program. For Hindi speakers, this Hindi Playlist - https://youtube.com/playlist?list=PL_aMuHABgX0iUJ11svagyHeAmPvOfpo0m&si=bZcPgkE_ZvUZWCks is tailored to provide relevant information in Hindi. Apart from this you can reach out to our alumni network. We are proud to have alumni working at some of the top tech companies in the world. They are a valuable resource for understanding their experiences and reviewing our program. You can connect with them and learn more about their journey with Scaler by visiting our alumni review page at: https://www.scaler.com/review/ For those who have enrolled for the Scaler NSET exam, we offer dedicated support. You will receive an email ID and a support number to assist with any queries or issues you may face before or during the exam. Please note that detailed counselling sessions, involving both parents and students, are exclusively conducted for candidates who successfully clear the test and interviews. Once you receive an offer, your assigned admissions counsellor will reach out to you for further guidance and support."},
    {"question": "Can I visit the campus?", "answer": "We're excited to offer you the opportunity to explore our campus and gain a firsthand understanding of our learning environment. Here's what you need to know about planning a visit: Location and Accessibility: The Scaler School of Technology is located in the heart of Bangalore, known as the Silicon Valley of India. Our campus's strategic location amidst numerous tech companies offers a unique advantage, providing students with close proximity to the thriving tech industry. Location : https://maps.app.goo.gl/61uwcRjrAT8nSVhT7 Campus Visits: We regularly organize trips to both our main and micro campuses. These visits are a great way for you to experience our state-of-the-art facilities, get a glimpse of our well-equipped hostels also known as our Micro-campus, and immerse yourself in our vibrant campus community. It's an excellent opportunity to see firsthand what makes Scaler School of Technology a special place for learning and innovation. How to Stay Informed: To stay updated on upcoming campus visits and to register, please keep an eye on our events page. Here, you'll find detailed information about scheduled visitation opportunities and instructions on how to sign up for them https://www.scaler.com/school-of-technology/events In addition to the opportunities for campus visits, we also have a fantastic resource for you to experience our campus virtually. We encourage you to watch these videos on YouTube, which offer an insightful tour of our facilities and a sense of the vibrant atmosphere on campus: 1. Scaler School of Technology Campus Tour/Walkthrough - https://youtu.be/QvZk_ZZniac?feature=shared 2. A Day in the Life at Scaler School of Technology - https://www.youtube.com/watch?v=YhAmiPnX1m0 These videos will provide you with a firsthand look at our state-of-the-art facilities, well-equipped hostels, and the overall environment that fosters learning and innovation. Discover the vibrant student life at SST! Dive into all the exciting activities, culture, and experiences our campus has to offer by visiting: https://www.scaler.com/school-of- technology/campus-life/"},
    {"question": "Why should I join a new institution like Scaler School Of Technology?", "answer": "Watch this video - https://youtu.be/XHms088oDHw?si=h_Hh8EfFRlQAidzu Scaler School Of Technology's parent company, Scaler, was established by Anshuman Singh and Abhimanyu Saxena. Both bring a wealth of experience from leading U.S. tech start-ups – Meta and Fab.com. Over the last 9 years, Scaler has successfully upskilled over 40,000 working professionals. Anshuman Singh, a trailblazer in the Indian tech scene, received multimillion-dollar offers from Facebook and Google in 2009. He has also worked closely with Mark Zuckerberg, leading the team that built Facebook Messenger and establishing Facebook's office in London. Our leadership team includes individuals from top companies like Amazon, Facebook, and Myntra. Bhavik Rathod, for example, built Uber in India from the ground up, scaling it from 0 to 4,000 employees. Scaler also boasts a network of over 1,200 employer partners, ensuring strong industry connections. Scaler School of Technology has already helped 110+ students secure internships in its first year, placing them in top companies like Swiggy, Neosapien, Pazcare, Freecharge, Allen Digital, and Rocketium. With a valuation of ₹6,000 crores, Scaler has been revolutionizing tech education since its inception in 2014. The company is backed by ₹650 crore in investments from global investors like Sequoia Capital and Tiger Global Capital and is endorsed by prominent figures like Kunal Shah (Founder - CRED), Deepinder Goyal (Founder - Zomato), and Binny Bansal (Founder - Flipkart). Scaler's credibility has even been recognized by government officials such as Amitabh Kant, former CEO of NITI Aayog. Scaler School of Technology has garnered recognition from prestigious publications and platforms, including being featured in TIME Magazine and Statista's \"World's Top EdTech Companies of 2024\" ranking. Additionally, Codeforces has ranked Scaler School of Technology among the Top 40 Colleges in India—an extraordinary accomplishment achieved within just its second year of operation."},
    {"question": "Why should I choose SST over low-demand branches at NIT/IITs?", "answer": "Watch this video by Anshuman- our founder on this topic : https://www.youtube.com/watch?v=szKs9fth9bo In the field of technology education, the importance of skills over institutional prestige is becoming increasingly evident. Graduates from IITs and NITs are often recognized for their smart peer groups, but in the tech industry, having strong skills is key to securing the best placement opportunities. This shift is evident in the hiring practices of companies like Facebook, where employees are selected for their expertise rather than their educational background, with many successful hires not originating from IITs. When comparing low-demand branches of engineering with computer science, there's a clear discrepancy in career prospects and earning potential. Students excelling in core engineering disciplines such as chemical or mechanical often face limited scope and a lower salary cap compared to their counterparts in computer science. This disparity is partly due to outdated curricula in top universities, which have seen little evolution in the past 15-17 years. Scaler, a tech education company, stands out in this landscape. In the last 4-5 years, Scaler has placed 5000 graduates in the industry. These graduates are sought after by top tech firms like Amazon, Microsoft, Google, and Facebook. Notably, Amazon has frequently hired more graduates from Scaler than all IITs combined in certain years. Please note that this data is with respect to Scaler, the the parent company of Scaler School of Technology as SST itself has yet to have it's first placement season. The opportunities in computer science, especially with a modern and relevant curriculum, far surpass those in less demanded engineering branches. Scaler's School of Technology exemplifies this, offering a program that not only focuses on current industry needs but also provides a peer group and learning environment conducive to success in the fast-evolving tech sector."},
    {"question": "What does a day look like for a student at SST?", "answer": "At Scaler School of Technology, each day is a unique journey of learning and growth, preparing students for long-term success. However, we can outline a general structure of their daily schedule: 1. Morning Routine: Students begin their day with breakfast, arriving at the macro campus by 9 AM. 2. Lectures and Modules: The academic day starts with lectures covering two different modules, ensuring diverse learning each day. 3. Lab Sessions and Assignments: After lectures, students engage in lab sessions and work on assignments related to the modules studied. 4. Instructor and Batch Success Manager Support: Throughout the day, students are accompanied by instructors and batch success managers. These mentors provide academic guidance, assist with assignments, and offer support for any challenges students face 5. Physical Wellbeing and Relaxation: Students have access to gym facilities, perfect for staying fit and energized. Weekends often feature recreational activities like sports or swimming, offering a balance between studies and physical health. 6. Cultural Celebrations: The campus comes alive during festivals like Diwali and Independence Day, with vibrant celebrations that foster community spirit. 7. Social and Culinary Experiences: For quick snacks or meals, the area around the micro campus offers a variety of affordable dining options, allowing students to unwind and socialize. 8. Club Responsibilities and Personal Development: Post-academic sessions, students focus on their club responsibilities, which play a crucial role in their holistic development. This structured yet dynamic schedule ensures that students at SST are constantly engaged in a stimulating educational environment, tailored to nurture their skills and prepare them for a successful future. Discover the vibrant student life at SST! Dive into all the exciting activities, culture, and experiences our campus has to offer by visiting: https://www.scaler.com/school-of-technology/campus-life/"},
    {
        "question": "What is the batch profile for the last year?",
        "answer": "Last year over 12,000 candidates took the Scaler NSET, and 440 were selected, indicating that last year our selection rate was 3.7%.\n\nMore than 137 students from the batch hold offers from prestigious institutions such as IIT, IIIT, NIT, BITS Pilani, University of Toronto, University of Waterloo, and more.\n128+ students achieved above 90 percentile in JEE with the highest going up to 99.4%.\n\nInterests and Expertise:\nStudents have a strong inclination towards technology and specialize in various tech-related fields.\nKey areas of interest include Competitive Coding, Application Development, Hackathons, Robotics, Artificial Intelligence, Cyber Security, Open Source, and Entrepreneurial Innovation.\n\nDemographics:\nThe demographic spread of students includes significant representations from different regions of India, with Maharashtra, Karnataka, Uttar Pradesh, Delhi NCR, and Telangana being the top locations.\nStudents predominantly come from Tier 1 and Tier 2 cities, comprising 31.6% and 28% of the demographic, respectively, with the rest categorized as 'Others'.\n\nAcademic Background:\nA majority of the students completed high school in the years 2022 and 2023, accounting for 43.5% and 45.1% of the batch, respectively.\nSmaller percentages completed high school in the years 2021 and before 2020, at 6.7% and 4.7%, respectively.\n\nExplore the detailed batch profile of 2023 batch here - https://docs.google.com/presentation/d/1kU2XK2s8rDqzfdc96dI6gNv2ng8ecqZV/edit#slide=id.g27b3458c5fd_0_300\nYou can watch students talk about their backgrounds: https://youtu.be/cXO6BJk6AyY?si=8ui2fSQdYYIF7UWb\nConnect with the current students to learn more about SST- https://bit.ly/3yNPVAc"
    },
    {
        "question": "Tell me about last year's batch",
        "answer": "Last year in 2023 there were more than 54,000 registrations for admission.\nOut of these, over 5,000 candidates took the Scaler NSET, and 200 were selected, indicating that last year our selection rate was 3.8%.\nMore than 60 students from the batch hold offers from prestigious institutions such as IIT, BITS Pilani, Purdue University, IIIT, NIT, University of Waterloo, and more.\n\nThe students have impressive academic records, with a median Class X and Class XII score of 91% and 85% respectively.\n\nInterests and Expertise:\nStudents have a strong inclination towards technology and specialize in various tech-related fields. However a large group also come from non-coding backgrounds.\nKey areas of interest include Competitive Coding, Application Development, Hackathons, Robotics, Artificial Intelligence, Cyber Security, Open Source, and Entrepreneurial Innovation.\n\nDemographics:\nThe demographic spread of students includes significant representations from different regions of India.\n\nExplore the detailed batch profile here - https://docs.google.com/presentation/d/1kU2XK2s8rDqzfdc96dI6gNv2ng8ecqZV/edit#slide=id.g27b3458c5fd_0_300\nYou can watch students talk about their backgrounds: https://youtu.be/cXO6BJk6AyY?si=8ui2fSQdYYIF7UWb\nConnect with the current students to learn more about SST- https://bit.ly/3yNPVAc"
    },
    {
        "question": "Apart from academics what other activities can students expect?",
        "answer": "Watch this video to know more - https://youtu.be/cgNgSoZbm6o?feature=shared\n\nSST encourages students to participate in a variety of extracurricular activities that promote personal growth and community engagement. These include sports, cultural celebrations, coding clubs, and tech competitions.\n\nStudents can join clubs such as the Sports Club, Cultural Club, Open Source Club, TED Talk Tribe, and Competitive Programming Club. These clubs allow students to explore their intellectual, creative, and physical interests while contributing to campus life.\n\nApart from this there are:\n1. Cultural Events: Celebrations of festivals and cultural events like Independence Day, enhancing community engagement.\n2. Social Interaction: Socializing with peers at dining spots around the campus, promoting a vibrant social life.\n\nDiscover the vibrant student life at SST! Dive into all the exciting activities, culture, and experiences our campus has to offer by visiting: https://www.scaler.com/school-of-technology/campus-life/"
    },
    {
        "question": "What's the value of an online degree? What if a student goes for off-campus placement, will this degree hold the same value as a normal degree?",
        "answer": "Yes, this Bachelor's degree from IIT Madras / BITS Pilani is fully valid and accepted by most good tech companies for placements. You can verify the same in the FAQ section of UGC website (Q4) - https://deb.ugc.ac.in/FAQ\n\nScaler School of Technology (SST) offers a fully offline 4-year program in Bangalore, where all teaching is conducted in person by expert instructors from top tech companies like Amazon, Meta, Google and more. This hands-on approach, coupled with rigorous assignments and exams ensures the highest standard of education and assessment integrity.\n\nParallelly, SST students pursue a UGC-recognized degree from either BITS Pilani or IIT Madras, both of which are widely accepted for jobs, higher studies, and government exams.\n\nWatch this video where our founder, Anshuman Singh explains the rationale around placements: https://www.youtube.com/watch?v=mxeKIZEH6V4\n\nFor all types of placements - be it on-campus or off-campus, what truly matters is your skills, portfolio, and interview performance — not whether your degree was online or offline.\n\nSST students are likely to get jobs at good companies and roles due to several reasons:\n1/ High Talent Density Attracts Top Companies: SST admits a concentrated group of high-performing CS students, making it an efficient recruiting ground for companies seeking top-tier talent.\n\n2/ Coding Culture: Students actively engage in ICPC, GSoC, open source, and coding clubs — fostering a hands-on, innovation-driven environment that attracts top tech recruiters.\n\n3/ Bangalore Advantage: Being in Bangalore, SST offers easy access to tech companies for placements, internships, and ongoing industry interaction.\n\n4/ Scaler's Alumni Network: SST students tap into Scaler's 40,000+ alumni community, including professionals at Microsoft, Amazon, and more — enabling stronger referrals and long-term career growth.\n\nAs of now, 92%+ of SST's founding batch has already got paid internships across companies like Zomato, Swiggy, Freecharge, Dukaan, Pazcare etc., with a few international offers in the pipeline now.\n\nRegarding placements, our robust online program at Scaler- the parent company of Scaler School of Technology, successfully places approximately 200 learners each month, leveraging our extensive network of over 1200 companies."
    },
    {
        "question": "Can I get a refund for the NSET fee?",
        "answer": "We generally do not offer refunds for the NSET Test fee. Our policy is to maintain a firm stance on this to ensure fairness and consistency for all applicants. However, we do acknowledge that there may be exceptional circumstances that warrant a reconsideration of this policy. In such rare cases, we encourage you to reach out to us with specific details of your situation. Each request for a refund under exceptional circumstances will be evaluated on a case-by-case basis to determine if it meets the criteria for a refund exception.\n\nPlease note that these exceptions are highly unusual and granted only under specific, extenuating circumstances. If you believe your situation qualifies, please contact our support team with all relevant information and documentation to support your request."
    },
    {
        "question": "Why should I choose to pursue Computer Science?",
        "answer": "Watch this video : https://www.youtube.com/watch?v=HMY8l4WagCU\n\nWhen selecting the right branch of engineering, there are several key factors to consider:\n\nPersonal Interest and Passion: The most important factor is your own interest and passion for a particular field. If you have a clear idea of what excites you, this should guide your decision. However, it's common for many students to be uncertain about their interests at this stage.\n\nDemand in the Field: Observing the last two decades, there's been a significant shift towards digital solutions in various sectors. This change has led to an increased demand for computer science graduates. From everyday applications like Uber, Ola, Swiggy, Zomato, and Google Maps, it's evident that software engineering plays a pivotal role in modern life. The trend indicates a continuous digitization across domains, creating a considerable demand for expertise in computer science.\n\nSalary Considerations: There is a notable disparity in salary between computer science graduates and graduates from other engineering branches. For instance, computer science graduates from top institutes often have starting salaries above 20 lakhs, whereas other engineering disciplines tend to have lower average salaries and sometimes less comprehensive placement rates.\n\nFuture Prospects of Computer Science: Despite some concerns about saturation, the field of computer science is projected to grow substantially. Forecasts, like those from Coursera, suggest the creation of millions of new jobs in software engineering. The evolution of technology, especially in AI and machine learning, is changing the nature of jobs and increasing the integration of software engineering into other fields, including traditional engineering disciplines.\n\nStrategic Starting Point: Choosing the right engineering branch can significantly impact your career trajectory. A field like computer science, which is less competitive and has more opportunities, can provide a solid foundation for success. In contrast, entering a field with fewer opportunities and greater competition can present more challenges.\n\nIn summary, when deciding on an engineering discipline, it's crucial to balance personal interests with the practical aspects of demand, salary potential, and future job prospects. Thorough research and consideration of these factors will help in making a well-informed decision."
    },
    {
        "question": "What degree does one get after graduating from Scaler School of Technology?",
        "answer": "Watch this video to understand all about degrees & job prospects at SST- https://www.youtube.com/watch?v=qh8VHFuoJcQ\n\nAt Scaler School of Technology, we strive to provide our students with a competitive edge in Computer Science and AI by offering a skill-focused program, complemented by prestigious degrees and a strong brand value:\n\nSingle Degree Program:\nOption A: 4-Year B.S. Degree in Data Science & Applications from IIT-Madras, (OR)\nOption B: 4-Year BSc (Hons.) Degree in Computer Science from BITS Pilani.\n\nDual Degree Program:\nOption A: 3-Year BSc Degree in Programming & Data Science from IIT-Madras, followed by a 1-Year MS from Woolf, (OR)\nOption B: 3-Year BSc Degree in Computer Science from BITS Pilani, followed by a 1-Year MS from Woolf.\n\nScaler School of Technology (SST) students can apply to B.S. Degree in Data Science & Applications from IIT Madras and pursue this degree in parallel at SST's Undergraduate program campus in Bangalore. The IIT Madras degree is awarded separately, and admission to the degree program is solely at the discretion of IIT Madras. Students must meet all requirements set by IIT Madras to earn this degree.\n\nStudents have also the opportunity to apply to the Bachelor of Science in Computer Science by BITS Pilani which an Institute of Eminence recognized by the University Grants Commission (UGC).\n\nSimilarly, the Master of Science in Computer Science is obtained from Woolf, a globally recognized European higher education institution. This degree is endorsed by the European Credit Transfer and Accumulation System (ECTS), a widely recognised accreditation system accepted globally.\n\nThese industry-recognized degrees enable our graduates to explore job opportunities with leading technology companies worldwide, eligibility for exams like GRE, GMAT, CAT, Civil Services exams and qualify for government jobs and further studies both within India and abroad."
    },
    {
        "question": "Are the degrees recognized by UGC or approved by AICTE?",
        "answer": "Yes the degree options via IIT Madras and BITS Pilani are recognized by UGC and considered equivalent to convetional degrees. SST provides flexible degree options with top institutions to ensure students gain the best educational foundation: Single Degree Program: Option A: 4-Year B.S. Degree in Data Science & Applications from IIT-Madras, (OR) Option B: 4-Year BSc (Hons.) Degree in Computer Science from BITS Pilani.\nDual Degree Program:\nOption A: 3-Year BSc Degree in Programming & Data Science from IIT-Madras, followed by a 1-Year MS from Woolf, (OR)\nOption B: 3-Year BSc Degree in Computer Science from BITS Pilani, followed by a 1-Year MS from Woolf.\nBS in Data Science and Applications, IIT Madras:\nThis degree program operates independently and Scaler School of Technology (SST) students can apply to and pursue this degree in parallel at SST's Undergraduate program campus in Bangalore . The IIT Madras degree is awarded separately, and admission to the degree program is solely at the discretion of IIT Madras. Students must meet all requirements set by IIT Madras to earn this degree. More details can be found [here]. The BS in Data Science and Applications, offered by IIT Madras, is an official degree approved by the Senate of IIT Madras, which has the power to award degrees as per The Institutes of Technology Act, 1961. Hence, this degree would meet the requirement of any study or job that accepts a Bachelor of Science (BS) degree.\nB.Sc. Computer Science, BITS Pilani:\nThe B.Sc. Computer Science degree from BITS Pilani is recognized and approved by the University Grants Commission (UGC), making it a UGC-approved degree. This recognition enables you to pursue various master's degrees in science, management, arts, and other fields. It also allows you to apply for exams like CAT, GATE, UPSC, GRE, GMAT, and more. Unlike some engineering colleges, the B.Sc. degree from BITS Pilani does not require approval from the All India Council for Technical Education (AICTE). This is because BITS Pilani is an Institute of Eminence, accrediting its B.Sc. degree.\nWatch this video to understand why SST does not provide a B.Tech Degree- https://www.youtube.com/watch?v=mxeKIZEH6V4\nM.S Computer Science, Woolf University:\nWoolf University, being a European university, is not required to have UGC or AICTE approvals as mandated in India. However, Woolf is accredited by educational credential assessment (ECA) organizations in Europe, USA, and Canada, which serve similar functions to UGC in India. This accreditation provides various benefits when applying to universities in those regions, as well as when seeking visas and jobs. Additionally, Woolf is accredited with the European Credit Transfer System, allowing you to skip any courses you have already completed with Scaler while pursuing higher studies at UK universities."
    },
    {
        "question": "What financing options are available for paying admission fees if I get selected?",
        "answer": "Watch this video : https://youtu.be/Jiit1yVb2oY?si=PmUwDkd_rx9yqxva&t=1321 .We provide several financing options based on your needs and background through partnerships with Banks and NBFCs. Once you receive an offer, our admissions team will be able to assist you with the same."
    },
    {
        "question": "What is the fee structure of the program?",
        "answer": "The fees for each year of the program at Scaler School of Technology include Admission, Tuition, Hostel & Mess Fees. For detailed information regarding fees, you can visit the following link: https://www.scaler.com/school-of-technology/admission/ .Please note that the fees are subject to change in the future. Scaler School of Technology also offers scholarships and financial aid options to eligible students."
    },
    {
        "question": "What career outcomes can one expect after graduating from Scaler School of Technology?",
        "answer": "Watch this video : https://youtu.be/wADh1LbUzMk?si=mrBJTLm5wt-d2ueG\nSST graduates will emerge well-prepared for the tech industry, armed with essential skills for success. Additionally, students may secure pre-placement offers after their 1-year cumulative industry immersion. They'll also build proof of work while developing 50+ products during the programme. All these unique aspects of Scaler School of Technology enable our graduates to have a strong resume and give them an edge during the recruitment process for leading tech companies.\nAlready 110+ students have secured internships in top tech companies and more. Students also receive support and guidance for their own entrepreneurial venture - 10+ students have started their own ventures.\nTop reasons why recruiters are showing interest in SST graduates: \nHigh-Quality Graduates: Our selective admissions and focus on computer science ensure a pool of highly skilled graduates, making SST a top choice for efficient recruitment. Vibrant Coding Culture: Our dynamic coding culture, desire to get students to participate in ICPC and GSoC, and active student clubs, make us appealing to leading tech companies. Strategic Location: Situated in Bangalore – the epicentre of India's tech industry, it offers logistical benefits for campus recruitment and internships, enhancing student and recruiter experiences.\nCareer and Networking Benefits: The depth of experience and the extensive alumni network of over 40,000 working professionals, including those at companies like Microsoft and Amazon, provide significant advantages in career progression and access to referrals."
    },
    {
        "question": "Is this a fully residential program?",
        "answer": "You can watch this video to understand why the course is residential : https://youtu.be/cgM3a2j-eQI?si=qjCx0hwszVB085mw\nWatch these videos to see the campus : https://www.youtube.com/watch?v=MIj3eq0HsVI\nhttps://www.youtube.com/watch?v=YhAmiPnX1m0\nYes, the Computer Science program at the Scaler School of Technology is a full-time on-campus program. The campus is located in the heart of the silicon valley of India, Bangalore. Being situated amidst numerous tech companies, the campus provides students with a unique advantage of being in close proximity to the tech industry.\nThe campus's strategic location ensures that students are constantly exposed to the dynamic tech ecosystem. They can witness the latest innovations and advancements happening in nearby tech companies. This exposure helps students stay updated with emerging technologies, industry trends, and best practices, giving them a competitive edge in their careers.\nGet a glimpse of our state-of-the-art facilities, hostel amenities, and vibrant campus community. We invite you to take a few minutes to watch this video: \nDiscover for yourself what makes Scaler School of Technology such a unique and inspiring place to learn."
    },
    {
        "question": "Who will be the faculty of the course?",
        "answer": "To know more about Scaler School of Technology's esteemed faculty members and their expertise, we recommend watching the following video: https://youtu.be/3Jl9VyI4_X8?si=vAvC9fRjAVVKcmmT&t=264\nAt Scaler School of Technology, our faculty forms the foundation of learning. We prioritize helping students learn directly from industry experts who have achieved remarkable success in the tech industry.\nAt Scaler, our teaching structure is built upon four pillars:\nInstructors: Daily classes led by industry professionals who have developed products for renowned companies like Facebook, Amazon, and Zomato.\nMentors: Industry experts offering monthly personalized sessions to shape students' career paths.\nSuccess Managers: Supportive guides assisting with doubt-solving, assignments, and overall well-being.\nSuper Mentors: Industry leaders, including notable figures like Rajan Anandan, Apurva Khandelwal, and Rishabh Bansal, who serve as mentors and guides for the entire course."
    },
    {
        "question" : "What is the eligibility criteria for Scaler School of Technology?",
        "answer" : " To know more about Scaler School of Technology's eligibility criteria, we recommend watching the following video: https://youtu.be/YteUoBU4yI4 .The Scaler School of Technology welcomes students who have completed their Class XII exams in 2025 or earlier, provided they are under the age of 20. This age limit allows us to focus on delivering a tailored educational experience for young individuals who are at a critical stage in their academic journey. Admission offers are contingent upon having mathematics as a subject in XII and achieving a mathematics score of above 60%, along with passing XII finals. To apply for the program at Scaler School of Technology, please visit our official website at:  https://www.scaler.com/school-of-technology/"
    },
   
  {
    "question": "How can I apply for the SST program?",
    "answer": "Watch this video to understand the process: What is the admissions process in Scaler School of Technology? - https://youtu.be/YteUoBU4yI4?feature=shared\n\nThe application process for Scaler School of Technology consists of three essential steps:\n\nStep 1: Complete the application form by providing all the necessary details and information accurately. This step ensures that we have a comprehensive understanding of your background and qualifications.\n\nStep 2: Attempt the NSET (Scaler's entrance test) with full dedication and commitment. The NSET assesses your skills and knowledge in Math and Logical Reasoning.\n\nStep 3: Upon successfully clearing the NSET, you will advance to the final round, which is the personal interview round. This round provides an opportunity for us to have a face-to-face interaction, delve deeper into your aspirations and goals, and assess your suitability for admission to Scaler School of Technology.\n\nStudents can also be selected through profile-based criteria, where we consider one or more of the following:\n1. Outstanding academic performance in X and XII, especially in Mathematics\n2. High percentile in competitive exams\n3. Notable achievements in tech competitions like IOI, Codechef, and hackathons\n\nYou can start your application here: https://www.scaler.com/school-of-technology/application"
  },
  {
    "question": "What makes SST's undergraduate program stand out as one of the best in the country?",
    "answer": "To truly understand how our program stands out, we invite you to hear from our director: https://www.youtube.com/watch?v=3Jl9VyI4_X8\n\nAt SST, we prioritize three key aspects: learning outcomes, the quality of instructors, and career outcomes.\n\nOur program ensures graduates have skills equivalent to a Senior Engineer/SDE-II and more than a year of industry experience. It is structured into three phases:\n\n1. Initial 2 Years: Learn fundamentals of DSA, Fullstack, Shell, and Frontend; develop soft skills.\n2. Next 1 Year: Specialize in AI/ML, Algo Trading, etc., and secure placement offers.\n3. Final 1 Year: 1-Year industry immersion through internships or startup/project work.\n\nOur instructors are industry veterans from top companies like Facebook, Amazon, and Zomato. We also offer personalized guidance and access to 1200+ career partners for job opportunities."
  },
  {
    "question": "Can I do a Masters after the program?",
    "answer": "Yes, upon completing the program at Scaler School of Technology, you have excellent opportunities to pursue a Master's degree both in India and internationally.\n\nWatch this video by our Founder, Anshuman to learn more: https://youtu.be/mxeKIZEH6V4?t=951\n\nSST students have these degree options:\n\nSingle Degree Program:\n- Option A: 4-Year B.S. Degree in Data Science & Applications from IIT-Madras\n- Option B: 4-Year BSc (Hons.) Degree in Computer Science from BITS Pilani\n\nDual Degree Program:\n- Option A: 3-Year BSc from IIT-Madras + 1-Year MS from Woolf\n- Option B: 3-Year BSc from BITS Pilani + 1-Year MS from Woolf\n\nGraduates of the 4-year SST program in Bangalore can apply for most Master's programs worldwide. Always check the specific university's eligibility requirements."
  },
  {
    "question": "Am I eligible for government jobs after graduating from Scaler School of Technology?",
    "answer": "Watch this video: https://youtu.be/mxeKIZEH6V4?t=1043\n\nYes, you are eligible for most government jobs. Our Bachelor's degrees from IIT Madras or BITS Pilani are UGC-approved and recognized.\n\nThe BS in Data Science and Applications from IIT Madras is officially approved under The Institutes of Technology Act, 1961.\nThe BSc in Computer Science from BITS Pilani is awarded by an Institute of Eminence recognized by the UGC.\nThe MS from Woolf is accredited under the European Credit Transfer System (ECTS).\n\nThese degrees qualify you for government exams, higher education, and public sector jobs. However, eligibility may vary, so check the official job portal of your target institution."
  },
  {
    "question": "If I want to pursue a master's abroad, will this degree be accepted by other colleges?",
    "answer": "Watch this video: https://www.youtube.com/watch?v=mxeKIZEH6V4&t=950s\n\nYes, absolutely.\n\nAll SST students are enrolled in a UGC-recognized bachelor’s degree from either IIT Madras or BITS Pilani. These degrees are accepted by institutions globally for pursuing Master’s programs.\n\nStudents may also opt for a Master’s degree from Woolf, an EU-accredited institution. It uses the ECTS credit system, which is widely accepted for postgraduate admissions worldwide.\n\nThat said, always verify with the specific university's official admissions page for eligibility criteria."
  },
  {
    "question": "Why did you use the degree structure (B.Sc. + M.S.) instead of the conventional B.Tech. degree?",
    "answer": "Watch this video to understand why SST decided to NOT provide a conventional B.Tech Degree: https://youtu.be/mxeKIZEH6V4?t=56\n\nTraditional BTech programs often have outdated curricula, minimal industry exposure, and faculty disconnected from modern tech practices. Most only offer a 2-month internship over 4 years.\n\nDespite producing 1.6 million engineers yearly, only 2% get jobs paying over ₹8 LPA.\n\nSST’s structure solves this by offering:\n1. Real-world, industry-led tech education at SST\n2. A UGC-recognized bachelor’s degree from IIT Madras or BITS Pilani\n3. An optional, globally accredited MS from Woolf, based on the ECTS system\n\nThis ensures students are industry-ready, eligible for jobs, higher studies, and government exams."
  },
   {
        "question" :" If a student's age is 20 as of June 30,2025, are they eligible to apply?",
        "answer" : " Yes, students who are under 20 years as of June 30 2025 are eligible to apply for the Scaler School of Technology program."
    },
    {
        "question" :"My boards result isn't out yet. I am expecting it soon. Can I still apply for SST?",
        "answer" : "Yes, you can still apply for the Scaler School of Technology (SST) even if your board exam results are not yet released. We understand that the results may be pending, but you can still proceed with the application process However, the admission offer is based on securing a Mathematics score of above 60% and final pass result of XII. Students will not be eligible for a refund if found to be ineligible. Make sure to provide the necessary information and documentation required during the application, and if necessary, you can update your results later once they are available"
    },
    {
        "question" :"I am a student who joined a polytechnic/diploma after class 10. Am I eligible to apply for the UG program at Scaler School of Technology?",
        "answer" : "At Scaler school of technology, we believe in making education accessible to all individuals. Our Undergraduate program primarily focuses on enhancing undergraduate education, we have specific guidelines for eligibility at the Scaler School of Technology.If you are under the age of 20 and fulfill the educational requirements, we welcome you to apply for our program, even if you joined a polytechnic or diploma program after class 10. However, please note that you would need to take admission in the first trimester or Year 1 of the four-year Undergraduate program.We understand that students come from diverse educational backgrounds, and we strive to provide opportunities for growth and learning to all motivated individuals. We encourage you to explore the possibilities at Scaler and take the first step toward building a successful career in the field of technology.Yes, as a diploma student you are eligible to apply. However, we do not have the option of starting in the 2nd year. All diploma students will need to start in the 1st year."
    },
    {
        "question" :"Can I join this program if I'm in the first year of B.Tech?",
        "answer" : "Yes, if you are currently in the first year of your B.Tech program, you are eligible to join the Scaler School of Technology program provided you are under 20 years as of June 30, 2025.However, please note that you would need to take admission in the first trimester or Year 1 of the four-year Undergraduate program as the credits earned in your current B.Tech program may not be transferable to the SST program.We understand that students come from diverse educational backgrounds, and we strive to provide opportunities for growth and learning to all motivated individuals. We encourage you to explore the possibilities at Scaler and take the first step toward building a successful career in the field of technology."
    },
    {
        "question" :"Can I enroll in this course if I'm a working professional without any undergraduate degree?",
        "answer" : "At Scaler, we are dedicated to ensuring that education is accessible to all individuals. While our program primarily focuses on enhancing undergraduate education, we specifically cater to individuals under the age of  20 at Scaler School of Technology.To enroll in our program, there are specific eligibility criteria that you need to meet. Firstly, you must have completed your 12th grade education in 2025  or earlier. Additionally, you should be under the age of 20  to be eligible for enrollment at Scaler School of Technology. If you fulfill these age and educational requirements, we welcome you to join our program and pursue your aspirations in the field of technology.We are deeply committed to providing a clear pathway for young individuals to develop their skills and thrive in the ever-evolving tech industry. By offering this opportunity, we aim to empower aspiring learners and support their journey towards success."
    },
    {
        "question" :"Can I enroll in this course if I'm currently doing a full-time course with Scaler and already have a degree in another stream?",
        "answer" : "At Scaler, we are dedicated to ensuring that education is accessible to all individuals. Although our program primarily focuses on enhancing undergraduate education, we specifically cater to individuals under the age of 20  at Scaler School of Technology.To enroll in our program, there are specific eligibility criteria that you need to meet. Firstly, you must have completed your 12th grade education in 2025  or earlier. Additionally, you should be under the age of 20  to be eligible for enrollment at Scaler School of Technology.If you fulfill these age and educational requirements, we welcome you to join our program and pursue your aspirations in the field of technology."
    },
    {
        "question" :"What is the application process?",
        "answer" : "To know more about the admissions process, please watch this video: https://youtu.be/YteUoBU4yI4?feature=shared.The application process for Scaler School of Technology consists of three essential steps.Step 1: Complete the application form by providing all the necessary details and information accurately. This step ensures that we have a comprehensive understanding of your background and qualifications.Step 2: Attempt the NSET (Scaler's entrance test) with full dedication and commitment. The NSET assesses your skills and knowledge in logical reasoning and math.Step 3: Upon successfully clearing the NSET, you will advance to the final round, which is the personal interview round. This round provides an opportunity for us to have a face-to- face interaction, delve deeper into your aspirations and goals, and assess your suitability for admission to Scaler School of Technology.The combination of a strong performance in the NSET and a positive outcome in the personal interview round will lead to an offer of admission to Scaler School of Technology. We take pride in selecting candidates who exhibit exceptional potential and a genuine passion for technology.We are also excited to announce the introduction of profile-based shortlisting alongside NSET.As part of the selection criteria, we will consider one or more of the following: 1⃣ Outstanding academic performance in X and XII, especially in Mathematics 2⃣ High percentile in competitive exams 3⃣ Notable achievements in tech competitions like IOI, Codechef, and hackathons .These criteria help us recognize and reward candidates with strong aptitudes in various academic fields. You can start your application here: https://www.scaler.com/school-of-technology/application"
    },
    {
        "question" :"How much is the application fees?",
        "answer" : "The application fee for our program is Rs. 1000. However, if you have been referred by a Scaler learner, you are eligible for a 50% waiver on the application fee. Students can retake the NSET three times in an admission cycle at a cost of Rs. 100 only per re-attempt.To apply for the program at Scaler School of Technology, please visit our official website at: https://www.scaler.com/school-of-technology/application"
    },
    {
        "question" :"I am unable to pay the fees and am facing errors.",
        "answer" : "If you are experiencing difficulties with the payment process or encountering errors, we recommend writing to us on admissions@sst.scaler.com . Our dedicated team will promptly reach out to you and provide assistance in resolving the issue."
    },
    {
        "question" :"Should I apply from my number or the candidate's phone number?",
        "answer" : "It is preferred to provide the candidate's number for future communication. Sharing the candidate's number ensures that all relevant information and updates regarding the application process, including interview schedules and admission decisions, are communicated directly to the candidate. This helps to streamline communication and ensure that important updates reach the concerned individual in a timely manner."
    },
    {
        "question" :"What is the syllabus for the Scaler NSET Exam?",
        "answer" : "The Scaler's National Scholarship & Entrance Test is designed to evaluate candidates in three distinct sections, each with its own cutoff score. The test duration is 2 hours, and the sections included are:Mathematics: The mathematics section evaluates the candidate's knowledge and problem-solving skills. It gauges their quantitative aptitude and ability to apply mathematical concepts to solve problems.Aptitude and Logical Reasoning: This section measures the candidate's logical reasoning skills, analytical thinking, and problem-solving abilities.The entrance test evaluates candidates' understanding of these subjects and their potential to excel in the field of computer science. The NSET test prep kit is available on our website. Once you complete your application and select an NSET slot, you will receive the prep kit.Watch this video to know more: https://youtu.be/_Vr_kjjaROw?feature=sharedNeed help preparing for each section of the Scaler NSET? Ace the NSET with our Recorded Prep Series and be among the toppers- https://bit.ly/3VlHtkM"
    },
    {
        "question" :"How can I prepare for NSET?",
        "answer" : "Watch this video for a full overview of the Scaler NSET and tips on how to enhance your prep : https://youtu.be/_Vr_kjjaROw?feature=sharedPreparing for the Scaler NSET (Scaler’s National Scholarship & Entrance Test) requires a strategic approach and familiarity with the exam syllabus and pattern. Here's a step-by-step guide to help you prepare effectively:NSET Prep Kit: Access the NSET Prep Kit provided by Scaler for comprehensive guidance and resources tailored specifically for the exam. The kit should include detailed information about the test and tips for successful preparation.NSET Recorded Prep Series: Ace the NSET with our Recorded Prep Series and be among the toppers- https://bit.ly/3VlHtkMWalkthrough of the Syllabus and Exam Pattern: Start by understanding the syllabus and exam pattern for the NSET. Refer to the NSET Prep Kit provided by Scaler, which includes a detailed breakdown of the syllabus. Take note of the topics covered in each section and the reasons behind their inclusion in the exam.Sample Questions and Solutions: To get a better understanding of the NSET sections, review sample questions for each section along with their solutions. This will help you become familiar with the question types and the approaches to solve them effectively.Different Approaches to Solving Each Section: Explore different approaches to tackle each section of the NSET. Techniques like skimming through the paper and planning, tackling easier questions first, or focusing on more challenging ones can be employed based on your strengths and preferences. Find the approach that works best for you.Additional Study Resources: Supplement your preparation by referring to other relevant study materials. These can offer a more comprehensive understanding of the topics and help you identify areas where you need to focus more.Remember to allocate sufficient time for practice and revision. Consistent effort and a systematic study plan will contribute to your success in the Scaler NSET. Good luck with your preparation!"
    },
    {
        "question" :"Are there any resources available for preparation for NSET?",
        "answer" : "Watch this video for a full overview of the Scaler NSET and tips on how to enhance your prep : https://youtu.be/_Vr_kjjaROw?feature=shared Yes, there are several resources available for preparing for the NSET: 1. NSET Prep Kit: This toolkit includes comprehensive information on the marks distribution for each section, a detailed syllabus, and a sample test paper.2. NSET Recorded Prep Series: Access the recorded prep series to review key concepts and strategies for acing the exam.Ace the NSET with our Recorded Prep Series and be among the toppers- https://bit.ly/3VlHtkM 3. Sample Questions and Solutions: Practice with sample questions to familiarize yourself with the question types and solving techniques. 4. Additional Study Resources: Supplement your preparation with relevant study materials for deeper understanding and targeted revision. These resources are designed to guide you through a thorough and effective preparation process."
    },
    {
        "question" :"How many attempts can I give?",
        "answer" : "You can retake the NSET up to 3 times and can attempt the interview round 2 times in an academic year. Students can retake the NSET three times in an admission cycle at a cost of Rs. 100 only per re-attempt.For detailed information regarding the test dates and other important details, please visit our admissions page at: https://www.scaler.com/school-of-technology/admission/"
    },
    {
        "question" :"When is the entrance test?",
        "answer" : "To know more about Important dates for the admissions cycle, please visit: https://www.scaler.com/school-of-technology/admission/"
    },
    {
        "question" :"Is this an online exam? Is it proctored",
        "answer" : "Yes, the Scaler NSET is an online exam. It is conducted in an online mode and follows a proctored setup. This means that the exam is administered remotely through a computer or laptop, and strict monitoring measures are in place to ensure the integrity and fairness of the exam. Proctors supervise the exam to prevent any instances of cheating or misconduct"
    },
    {
        "question" :"What happens if I don't get selected in Scaler NSET?",
        "answer" : "If you are not selected in the first intake, you can attempt the NSET again. You have the opportunity to attempt the NSET once every month until you have exhausted 3 NSET attempts or 2 Personal Interview attempts for the year. Few days after the exam results are declared, you will see the option of rebooking a slot for the next test on your dashboard. Students can retake NSET three times in an admission cycle at a cost of Rs. 100 only per re-attempt.To know more about Important dates for the admissions cycle, please visit: https://www.scaler.com/school-of-technology/application"
    },
    {
        "question" :"How can I request to reschedule my Scaler NSET?",
        "answer" : "Test re-schedule requests are not permitted. Only in the case of totally unavoidable circumstances like Medical Emergencies, Family Emergencies, Natural Disasters etc can one apply for a re-schedule by writing to admissions@sst.scaler.com with the necessary proof before 48 hours."
    },
    {
        "question" :"How can I get selected for the Scaler NSET?",
        "answer" : "To get selected for the Scaler NSET, you need to complete your application, choose a test slot, and prepare with the help of the NSET Prep toolkit and other provided resources. Give your best effort on the day of the exam to maximize your chances of selection.Watch this video : https://youtu.be/_Vr_kjjaROw?feature=shared "
    },
    {
        "question" :"Can I reapply/ give my test again if I get admission but don't get a scholarship?",
        "answer" : "A student can only have one NSET application active at any time. If they apply again, their previous application and scores are cancelled. This means they must give up any current offer before reapplying. Students can retake the NSET three times in an admission cycle at a cost of Rs. 100 only per re-attempt."
    },
    {
        "question" :"Should we take the test from home or a center?",
        "answer" : "The Scaler NSET is an online exam that can be taken from the convenience of your home or any other location of your choice. If you do not have access to a personal laptop, you may take the test from a cyber cafe or any other suitable location. The exam is conducted in a completely proctored setup to ensure a fair and secure testing environment. Giving the test from mobile is not allowed, and the laptop/PC should have a working camera."
    },
    {
        "question" :"How can I check the results of the Scaler NSET?",
        "answer" : "The results of the Scaler NSET are typically released within 2 weeks of the exam. You will be notified via email regarding your result, and instructions will be provided on how to access your results."
    },
    {
        "question" :"What is the selection crietria of NSET?",
        "answer" : "Watch this video for a full overview of the Scaler NSET : https://youtu.be/_Vr_kjjaROw?feature=sharedThe selection criteria for the NSET primarily involve two key aspects:Overall Percentile-Based Selection: Candidates will be evaluated based on their overall score, which will be percentile-based. This approach allows for a relative comparison among all applicants, and those scoring within a certain percentile range will be considered for further stages of the selection process.Exceptional Performance in Sections: Apart from the overall score, exceptional performance in individual sections holds significance. If a candidate achieves a score above 40% in any one of the three sections, irrespective of their scores in the other sections, they will be selected for an interview.These two criteria collectively contribute to the selection process for the NSET, aiming to recognize both overall competence and outstanding performance in specific sections among the applicants."
    },
    {
        "question" :"Can I take the NSET from my phone?",
        "answer" : "No, the NSET exam can only be taken on a PC/laptop with a working camera. It is conducted in a completely proctored setup to ensure integrity and fairness during the exam."
    },
    {
        "question" :"Why is there so much focus on mathematics in NSET?",
        "answer" : " At Scaler school of technology we recognize the vital importance of mathematics in various fields of study, particularly computer science and engineering.Mathematics serves as the fundamental building block for comprehending intricate algorithms, data structures, and problem-solving techniques.By placing significant emphasis on mathematics, the Scaler NSET aims to evaluate students' ability to learn and excel in the field of computer science. Acquiring a solid understanding and mastery of mathematical concepts are essential for success in the dynamic and rapidly evolving tech industry."
    },
    {
        "question" :"How will the Personal Interview happen?",
        "answer" : "Watch this : https://youtu.be/Yts9ae-nqyo?si=hB6CK6gHSX-5l7nQThe Personal Interview for the Scaler School of Technology (SST) program can be conducted in either in-person or online formats, depending on the circumstances and preferences of the candidates. The interview process aims to assess the candidate's suitability for the program and allows the evaluators to gauge their potential, aspirations, and affinity towards computer science. The specific details regarding the interview format, location, or platform (if conducted online) will be communicated to the candidates prior to the interview."
    },
    {
        "question" : "What kind of questions will be asked in the Personal Interview?",
        "answer" : "Watch this : https://youtu.be/Yts9ae-nqyo?si=hB6CK6gHSX-5l7nQ .The Personal Interview at Scaler School of Technology typically focuses on understanding the candidate's learning ability, aspirations, and affinity towards computer science."
    },
    {
        "question" : "Are there any resources available for preparation for the Personal Interview?",
        "answer" : "Watch this : https://youtu.be/Yts9ae-nqyo?si=hB6CK6gHSX-5l7nQ .Yes, we provide a Personal Interview Prep Kit once you have successfully cleared the NSET. This kit is designed to assist you in better preparing for your personal interview, bringing you one step closer to securing admission to Scaler School of Technology"
    },
    {
        "question" : "When will the interviews take place",
        "answer" : "The dates for the personal interviews are shared with candidates once they have completed the NSET."
    },
    {
        "question" : "When is the first batch starting?",
        "answer" : "Classes for the 2025 - 29 batch of the Scaler School of Technology program, are scheduled to commence in August 2025.  For more detailed information and specific dates, we recommend visiting our official website.  You will find comprehensive details about the admission process, important dates, and other relevant information related to the program on our website - https://www.scaler. com/school-of-technology/"
    },
    {
        "question" : "Can I apply for all Admission Cycles?",
        "answer" : "You can apply for NSET for a total of 3 times."
    },
    {
        "question" : "What curriculum will all be covered in the computer science course?",
        "answer" : "To understand the curriculum - watch this video - https://www.youtube.com/watch?v=6Xbf5Dt-Q2s .Our curriculum at Scaler School of Technology is designed to provide learners with a comprehensive skill set equivalent to that of a Senior Engineer/SDE-II."
    },

    {
        "question" : "What Does 'Work-Integrated Learning' Mean?",
        "answer" : "Scaler's work-integrated learning approach goes beyond traditional classroom education, offering a comprehensive curriculum that surpasses mere theoretical knowledge. Scaler School of Technology's work-integrated learning program mandates a 1-year internship for every student."
    },

    {
        "question" : "Why is there a 1-year Industry immersion? Is it compulsory?",
        "answer" : "Watch this video to understand this better : https://youtu.be/JKktsjEFLA4?si=46h-vFi-RW2bPJ03 .The 1-year immersion is a mandatory component of the program at Scaler School of Technology."
    },
    {
        "question" : "What happens if I do not get an internship at the end of 2 years?",
        "answer" : "In the rare case that a student does not receive an internship offer, Scaler School of Technology has a contingency plan in place."
    },
    {
        "question" : "Do I have an option to choose not to work during the Immersion period and continue the program?",
        "answer" : "No, Scaler School of Technology's work-integrated learning program mandates a 1-year immersion for every student"
    },

    {
        "question" : "What if I don't get a job after Scaler?",
        "answer" : "Watch this video : https://youtu.be/PaBVCSG50gI .At Scaler School of Technology, we understand that finding employment after completing the program is a top priority for our students. While we provide extensive placement support and have a strong network of over 1200 placement partners to maximize your opportunities, we recognize that individual circumstances can vary. Here's what we offer to address concerns if you don't secure a job immediately:Comprehensive Placement Guidance: We are committed to equipping you with the necessary skills and knowledge to excel in the job market. Throughout the program, we provide intensive training, mentorship, and career guidance to enhance your employability and help you stand out as a candidate. Expansive Placement Partner Network: Our vast network of over 1200 placement partners gives us access to diverse job opportunities across the industry. We leverage these connections to connect you with potential employers and facilitate interviews, increasing your chances of finding the right job.Alumni Support: Our commitment to your success extends beyond the program. As a Scaler alumnus, you gain access to our alumni network, which includes successful professionals across various domains. This network can provide valuable guidance, mentorship, and referral opportunities to help you navigate your career path.While we strive for all our students to secure employment after completing Scaler, individual circumstances can differ. If you find yourself facing challenges in your job search, we encourage you to reach out to our dedicated placement support team. They are available to provide personalized assistance, including resume reviews, interview preparation, and guidance on job search strategies.At Scaler, we believe in your potential and are committed to supporting you throughout your journey."
    },
    {
        "question" : "What's the difference between a mentor and a batch success manager?",
        "answer" : "At Scaler School of Technology, both mentors and batch success managers play distinct but equally important roles in supporting learners.Mentors are industry experts who provide personalized guidance to learners in their career development. They offer insights, share practical knowledge, and help learners navigate challenges in their chosen field. Their primary focus is on mentoring and imparting domain-specific expertise.Batch success managers, on the other hand, are responsible for ensuring the day-to-day success of learners in their courses. They provide doubt-solving sessions, administrative support, manage schedules, and address concerns."
    },

{
        "question" : "Can I change mentors or batch success managers if they don't fit me?",
        "answer" : "If a student feels that their mentor or batch success manager is not the right fit for them, Scaler School of Technology recognizes the importance of a supportive environment and allows learners to request a change if there is a valid reason.However, it's important to note that mentor or batch success manager changes are subject to availability and the school's internal policies. While every effort is made to fulfill such requests, it may not always be possible due to logistical constraints. The ultimate goal is to ensure that learners receive the best possible support and guidance throughout their learning journey at Scaler School of Technology."
    },

{
        "question" : "What financing options are available for paying admission fees if I get selected",
        "answer" : "Watch this video : https://youtu.be/Jiit1yVb2oY?si=PmUwDkd_rx9yqxva&t=1321 .We provide several financing options based on your needs and background through partnerships with Banks and NBFCs. Once you receive an offer, our admissions team will be able to assist you with the same."
    },

{
        "question" : "I come from a low-income family and want to join the Scaler School of Technology, but I have financial limitations. Will scholarships be provided for students from low-income families?",
        "answer" : "Watch this video : https://youtu.be/Jiit1yVb2oY?si=PmUwDkd_rx9yqxva&t=1321Scaler . School of Technology does offer scholarships for students, including those from low-income families. While the specifics of each scholarship vary, the selection process includes evaluating a student's performance in the Scaler NSET, personal interview, academic achievements, achievements in competitive exams like JEE, coding projects or awards, and the family's financial profile.As a student from a low-income family, your financial situation will be considered as one of the key parameters in the scholarship evaluation process. This means that if you perform well in the other areas of evaluation, such as NSET performance and academic achievements, your financial limitations could make you a potential candidate for a scholarship. Remember, the final decision for scholarship awards rests with the Scaler Impact Foundation and the sponsors, and it is based on a comprehensive review of all the parameters, including your family's financial profile. Therefore, it is important to ensure that all the information you provide during the application process is accurate and complete"
    },

{
  "question": "What are the types of scholarships does Scaler School of Technology offer?",
  "answer": "Scaler School of Technology (SST) offers two main types of scholarships to support deserving students:\n\n1. **Merit-Based Scholarships**\nThese scholarships are awarded based on academic excellence and achievements in extracurricular or technical fields. Eligibility is assessed based on:\n- Scores in Class X, Class XII, JEE, BITSAT, etc.\n- Participation and achievements in technical competitions, hackathons, or other extracurricular activities.\n- Additional weightage is given to female students to promote diversity in tech.\n\n2. **Need-Based Scholarships**\nThese scholarships are designed to support students facing financial challenges. Eligibility is determined by:\n- Family income (must be below ₹5 LPA).\n- Submission of school fee slips and income proof for verification.\n- A combination of financial need and academic performance.\n\nScholarships at SST are funded by the Scaler Impact Foundation, supported by industry leaders like Vijay Shekhar Sharma (Paytm) and Prasanna Sankar (Rippling).\n\nThe number of scholarships available for each category may vary based on the program and the number of qualified applicants. To increase your chances of securing a scholarship, we encourage eligible students to submit their applications well in advance of the deadline."
},


{
  "question": "How can I apply for scholarships?",
  "answer": "To apply for scholarships at Scaler School of Technology, follow these steps:\n\n1. **Complete the Scaler NSET**: Your performance in the Scaler’s National Scholarship & Entrance Test (NSET) plays a crucial role in the scholarship evaluation process.\n\n2. **Personal Interview**: Do well in the interview round. This interview will be recorded and reviewed by the scholarship sponsors.\n\n3. **Highlight Academic Achievements**: Include your academic records, especially your Class X and XII scores, in your application.\n\n4. **Showcase Achievements in Competitive Exams**: Add any achievements in exams like JEE or equivalent.\n\n5. **Demonstrate Excellence in Technology**: Include public tech projects, coding awards, or any significant accomplishments in tech.\n\n6. **Detail Your Family’s Financial Profile**: Provide accurate details of your family’s financial situation, as need is also a consideration.\n\n7. **Submit a Detailed Application**: Ensure your application is comprehensive, accurate, and includes all relevant details that support your case.\n\n8. **Await the Evaluation**: The top 15% of applicants based on these criteria will be considered for scholarships. The Scaler Impact Foundation and the sponsors will review the applications.\n\n🎥 *Watch this video to understand the process better:* https://youtu.be/4a3LyPiDVkk\n\nAll scholarships are awarded by the Scaler Impact Foundation, supported by industry leaders like Vijay Shekhar Sharma (Founder & CEO, Paytm), Prasanna Sankar (Founder, Rippling), and others. Final selection is at the discretion of the Foundation and based solely on the submitted information."
},


{
  "question": "Am I eligible for the scholarships for the entirety of 4 years?",
  "answer": "Scholarships at the Scaler School of Technology are initially awarded for a period of 12 months (1 year). However, students have the opportunity to receive scholarships for subsequent years based on their academic and overall performance.\n\nThe review process for scholarships in subsequent years takes into account:\n\n- **Academic Performance**: Measured as Continuous Grade Rating (CGR) in the program.\n- **Contribution to the Student Community**: Participation in clubs, extracurricular activities, and overall contributions to the campus community.\n\nEach year, your performance and contributions will be evaluated to determine if you continue to meet the criteria for scholarship renewal. It's important to maintain high academic standards and actively participate in the Scaler community to enhance your chances of receiving the scholarship for the entire duration of your 4-year program."
},


{
        "question" : "Are the scholarships applicable on tuition fees or the entire fees (tuition + hostel)?",
        "answer" : "Scholarships are applicable to the tuition fees only. "
    },
     {
    "question": "What are the food facilities available at the hostel?",
    "answer": "At Scaler School of Technology, we take great pride in our hostel's extensive food facilities, designed to cater to diverse dietary needs and preferences.\n\n- **Smart Food Booking System**: Students can pre-book meals using their smartphones, selecting from a varied menu tailored to individual preferences.\n\n- **Three Nutritious Meals Daily**: Breakfast, Lunch, and Dinner are provided. Each meal is carefully prepared by experienced chefs to ensure both nutrition and taste.\n\n- **Feedback-Driven Improvement**: Students can rate and provide feedback on meals, enabling continuous enhancements to the dining experience.\n\n- **Self-Cooking Option**: For students who prefer preparing their own meals, cooking facilities are available in the hostel.\n\nOur goal is to provide a wholesome and flexible dining experience that promotes health, satisfaction, and culinary exploration."
  },
  {
    "question": "What are the security measures provided?",
    "answer": "Scaler School of Technology prioritizes student safety with robust security protocols:\n\n- **Access Control Systems**: Only authorized individuals can enter the dormitories using secure access credentials.\n\n- **24-Hour Warden Presence**: A dedicated warden is stationed at the entrance of the hostel round the clock to monitor and verify entry and exit.\n\n- **Surveillance Cameras**: CCTV cameras are installed in key common areas and entrances to deter and monitor any security threats.\n\n- **Emergency Protocols**: Trained staff and predefined emergency procedures ensure quick and effective responses to any unforeseen incidents.\n\nThese measures are designed to ensure a safe and secure living environment for all residents."
  },
  {
    "question": "Why is it mandatory to live on campus?",
    "answer": "Living on campus at Scaler School of Technology is mandatory to foster a vibrant and inclusive learning environment. Here's why:\n\n- **Enhanced Peer Learning**: Living close to peers encourages collaboration, idea sharing, and academic support.\n\n- **Access to Campus Resources**: Students benefit from proximity to libraries, study areas, clubs, and student services.\n\n- **Community Building**: Participation in campus events, clubs, and shared experiences fosters lifelong friendships and a strong sense of community.\n\nWe believe that immersion in campus life significantly enhances personal and academic growth.\n\n🎥 *Watch the video on why it's mandatory to live on campus*: https://youtu.be/cgM3a2j-eQI?si=lGBKcyoNxDzgpvmp\n\n🏫 *Explore the new state-of-the-art campus*: https://youtu.be/QvZk_ZZniac?feature=shared\n\n🌟 *Discover campus life at SST*: https://www.scaler.com/school-of-technology/campus-life/"
  },
   {
    "question": "Why does Scaler School of Technology not have a sprawling campus spanning several acres like many other institutions?",
    "answer": "At Scaler School of Technology, our focus is on delivering a world-class educational experience rather than on the size of our campus.\n\n- **Strategic Location**: Our campus is located in the heart of Bangalore, India’s Silicon Valley, placing students in close proximity to leading tech companies.\n- **Industry Exposure**: This urban setting ensures frequent interaction with the tech industry, access to the latest innovations, and a competitive career advantage.\n- **Purposeful Investment**: We prioritize investing in essential infrastructure and educational tools that directly benefit student learning and outcomes.\n\n🎥 *Watch the campus reveal video*: https://youtu.be/QvZk_ZZniac?feature=shared\n🌐 *Explore student life at SST*: https://www.scaler.com/school-of-technology/campus-life/"
  },
  {
    "question": "What are the extracurricular activities?",
    "answer": "Scaler School of Technology offers a wide range of extracurricular activities to foster holistic student development:\n\n- **Technical Clubs**: Coding clubs, robotics clubs, and hackathons allow hands-on learning and collaboration.\n- **Cultural & Creative Arts**: Music, drama, dance, and cultural festivals help students explore and showcase their talents.\n- **Sports and Wellness**: Physical activities and fitness are encouraged through various sports and recreational opportunities.\n\n🎥 *Watch the video to learn more*: https://youtu.be/cgNgSoZbm6o"
  },
  {
    "question": "Can there be single sharing rooms available for a student?",
    "answer": "The primary accommodation at Scaler School of Technology includes double and triple sharing rooms. However, single sharing rooms may be available upon request and are subject to availability. Please note that an additional cost may apply for single occupancy."
  },
  {
    "question": "Does the campus have facilities for sports activities?",
    "answer": "Yes, Scaler School of Technology provides extensive facilities for sports and recreation:\n\n- **Outdoor Sports**: Through partnerships with local facilities, students can enjoy football, cricket, and more.\n- **Indoor Games**: The campus offers indoor options like pool, table tennis, carrom, and other games.\n\nThese facilities are aimed at encouraging physical well-being, team building, and relaxation.\n\n🎥 *Watch the campus tour*: https://youtu.be/QvZk_ZZniac?feature=shared\n🌐 *Discover student life*: https://www.scaler.com/school-of-technology/campus-life/"
  },
  {
    "question": "Are there any extra security measures in the girls' hostel?",
    "answer": "Yes, Scaler School of Technology has implemented enhanced security measures specifically for the girls' hostel. The dormitory has access control systems that restrict entry to authorized individuals only. Additionally, a 24-hour warden is stationed at the entrance to provide assistance, ensure safety, and respond to emergencies. These steps are taken to ensure a secure and comfortable environment for female students."
  },
  {
    "question": "Who should parents contact in situations of emergency?",
    "answer": "In case of an emergency, parents can contact the Facility Manager or the respective wardens assigned to the hostel blocks. There is a balanced presence of both male and female wardens. Additionally, Scaler has a dedicated Customer Support Center available from 11 AM to 8:30 PM, 7 days a week, to address any concerns or provide timely assistance."
  },
  {
    "question": "Are doctors available at the hostel/campus for emergency situations?",
    "answer": "Yes, Scaler School of Technology has a well-equipped medical facility on campus. Success Managers and wardens are trained to handle medical emergencies and provide initial care. Dedicated medical staff are available to ensure prompt medical support and attention for any health-related incidents."
  },
  {
    "question": "What are the hostel's entrance and exit times?",
    "answer": "Students must report to the hostel (Micro-campus) by 9 PM. After this, from 9 PM to 7 AM, students are not permitted to leave the hostel premises. Exceptions can be made in special circumstances with prior parental or guardian requests."
  },
  {
    "question": "Are there any clubs or fests at Scaler School of Technology?",
    "answer": "Yes, Scaler offers a vibrant student life with various clubs and cultural festivals. These include music, dramatics, and sports clubs, as well as events that promote cultural expression and community engagement.\n\n🎥 *Watch more*: https://youtu.be/cgNgSoZbm6o?si=AvBa6rtCX1M7jUXi\n🌐 *Explore student life*: https://www.scaler.com/school-of-technology/campus-life/"
  },
  {
    "question": "Are the boys and girls hostels located in separate buildings or blocks?",
    "answer": "Yes, boys and girls are accommodated in different blocks within the same campus to ensure privacy and security. Shared spaces like the mess, playground, and study areas are gender-neutral, promoting inclusivity while maintaining personal comfort and safety."
  },
  {
    "question": "Can boys and girls go to each other's rooms?",
    "answer": "No, boys and girls are not allowed to enter each other's rooms. This rule is in place to maintain privacy and ensure a safe and respectful residential environment. Additional security measures, such as access control and 24-hour wardens, are implemented in the girls’ hostel."
  },
  {
    "question": "Are day scholars allowed?",
    "answer": "No, Scaler School of Technology is a fully residential program. All students are required to live on campus to ensure a holistic and immersive learning experience."
  },
  {
    "question": "Are calculators allowed in NSET?",
    "answer": "Yes, physical calculators are allowed during the National Scholarship & Entrance Test (NSET), as long as they are visible on camera. However, mobile phone calculators are strictly prohibited."
  },

  {
    "question": "Can a student leave Scaler in the middle of the 4-year program and continue the BSc with BITS independently from the semester in which he/she left Scaler?",
    "answer": "While a student can discontinue their studies at Scaler, they cannot resume the BSc program with BITS from the same semester. Instead, they would need to reapply to BITS and start from year 1."
  },
  {
    "question": "I want to edit my application form but I am not allowed to go back. What to do?",
    "answer": "To modify your application, please email admissions@sst.scaler.com using the subject line 'Application Data Change Request' for accurate and prompt assistance."
  },
  {
    "question": "I can't find the test link to join my NSET exam.",
    "answer": "Log in using your phone number at https://www.scaler.com/school-of-technology/application and click on the ‘Join test’ button to access the exam."
  },
  {
    "question": "I am unable to login using my phone number.",
    "answer": "Log in using your registered email at https://www.scaler.com, verify it, and then go to https://www.scaler.com/school-of-technology/application. Use the 'forgot password' option if needed to reset access."
  },
  {
    "question": "Is this a full time or a part time degree?",
    "answer": "This is a full-time 4-year residential programme. Students pursue a Bachelors in Computer Science via IIT Madras / BITS Pilani and a Masters in CS & AI from Woolf, a European institute awarding globally accepted ECTS credits."
  },
  {
    "question": "Is there any section wise cut off in NSET?",
    "answer": "Yes, section-wise cut-offs exist and are dynamic. They are determined based on the overall performance of all candidates in each section for every intake."
  },
  {
    "question": "What are the timings for NSET exams?",
    "answer": "NSET exams are conducted in multiple time slots throughout the day. Candidates can choose the slot that best fits their schedule."
  },
  {
    "question": "Where can I give Scaler NSET? Is there any particular center for Scaler NSET?",
    "answer": "Scaler NSET is an online exam that can be taken from home. Ensure you have a stable internet connection and a quiet environment for the test."
  },
  {
    "question": "I haven't received the NSET Prep Kit. Can you assist me?",
    "answer": "Once your application is complete and you've selected a test slot, you will receive the NSET prep kit automatically from our website."
  },
  {
    "question": "I have not received the Sample Test Links. Can you assist me?",
    "answer": "You will receive the sample prep kit after completing your application and selecting a test slot."
  },
  {
    "question": "Where can I access and how to understand the Scaler NSET performance report?",
    "answer": "The performance report will be shared via email with your results. It includes 5 columns (Percent Score, Absolute Score, Total Questions, Attempted Questions, Solved Questions) and 4 rows (Math, Learnability, Aptitude, and Overall) for detailed insights."
  },
  {
    "question": "I did not receive the practice test results. Where can I get it?",
    "answer": "Test reports are sent automatically to the email you provided. Please verify that your email is correct and has been validated to receive the results."
  },
  {
    "question": "I want to use a referral code in an application. Where can I get a code?",
    "answer": "You can request a referral code from Scaler community ambassadors or current students. This also gives you a chance to learn more about the program firsthand."
  },
  {
    "question": "I want to refer a friend. How should I do this?",
    "answer": "Only community ambassadors, alumni, and current students can refer others. If you wish to become a campus ambassador, visit: https://www.scaler.com/school-of-technology/ca"
  },
  {
    "question": "When can I expect my results?",
    "answer": "NSET exam results are shared within one week of the test. Personal Interview (PI) results are announced between one to two weeks after the PI."
  },
  {
    "question": "When is the next NSET?",
    "answer": "The NSET exam is conducted once every month until August. You can take the exam up to 3 times in an academic year. For important dates in the admissions cycle, please visit: https://www.scaler.com/school-of-technology/admission/"
  },
  {
    "question": "Can Biology students apply for Scaler School of Technology?",
    "answer": "Yes, Biology students can apply. However, admission is only offered if the student had Mathematics in Class XII and scored above 60% in it, along with passing their XII finals. Please note: No refund will be issued if a student is found ineligible later."
  },
  {
    "question": "Can I apply after 11th?",
    "answer": "No, you must have completed your Class XII exams in 2025 or earlier to be eligible. Also, applicants must be under the age of 20 to apply. Apply here: https://www.scaler.com/school-of-technology/"
  },
  {
    "question": "Is it necessary to fill out the interview profiling form before the test?",
    "answer": "You must fill out the interview profiling form before the interview, not necessarily before the test. However, completing it earlier helps us better evaluate you and improves your chances for scholarship consideration."
  },
  {
    "question": "Is there any negative marking in Scaler NSET test?",
    "answer": "No, there is no negative marking in the Scaler NSET test."
  },
  {
    "question": " Do you require 60% in class XII only or both in class XII and XI to be eligible for Scaler School of Technology?",
    "answer": "No, you only need to have 60% in class XII to be eligible for Scaler School of Technology. It is not necessary to have 60% in both class XII and XI."
  },
  {
    "question": "Can I pay registration fees tomorrow",
    "answer": "To know more about important dates and deadlines for the admissions cycle, please visit: https://www.scaler.com/school-of-technology/admission/"
  },
  {
    "question": "What is the last date for the test?",
    "answer": "To know more about important dates and deadlines for the admissions cycle, please visit: https://www.scaler.com/school-of-technology/admission/#timeline"
  },
  {
    "question": "When can I register for NSET?",
    "answer": " To know more about important dates and deadlines for the admissions cycle, please visit: https://www.scaler.com/school-of-technology/admission/ Watch this video to understand the Scaler NSET registeration process: https://www.youtube.com/watch?v=_Vr_kjjaROw&t=68s"
  },
  {
    "question": "Can I do AI & ML (machine learning) course at SST?",
    "answer": "Yes, you can do an AI & ML course while in SST. During your last year at SST, you will have the opportunity to choose any two specializations, which include:\n• Engineering Leadership Track\n• MAANG Track\n• Algo Trading Track\n• AI/ML Track\nIf you opt for the AI/ML track, you will learn skills such as Probability and Statistics 2, Linear Algebra, Classical ML (Supervised Learning), Classical ML (Unsupervised Learning), Computer Vision, and NLP."
  },
  {
      "question" : "Is NSET compulsory?",
      "answer" : "Yes, NSET is compulsory if you want to take admission in Scaler School of Technology. "
   
   },
   {
      "question" : "I want a call back.",
      "answer" : "To learn more about Scaler School of Technology and have all your questions answered, join us in our weekly Q&A sessions where we address all your concerns and doubts. Register for free sessions here: https://www.scaler.com/school-of-technology/events"
   
   },
   {
      "question" : "Can I get admission in Scaler School of Technology through management quota?",
      "answer" : "No, Scaler School of Technology does not take admissions through the management quota. The only way to take admission in SST is through Scaler NSET."
   
   },
  {
  "question": "I am unable to get the verification email. What do I do?",
  "answer": "If you're not receiving the verification email, try the following steps:\n1. Check your spam or junk folder.\n2. Ensure that you entered the correct email address during registration.\n3. Wait a few minutes, as there may be a slight delay in delivery.\n4. If you still don’t receive it, try resending the verification email from the registration page.\n5. Make sure your email provider isn’t blocking mails from '@scaler.com'.\n\nIf the issue persists, please contact Scaler support for further assistance."
}
,
   {
      "question" : "I am unable to get the verification e-mail. What do i do?",
      "answer" : "Please ensure that the email address you have provided is correct. If the email is accurate, please wait for a few hours and attempt the verification process again. If the issue persists, kindly escalate it by sending an email to admissions@sst.scaler.com    "
   
   },
   {
      "question" : "I’m unable to upload my photo. How do I proceed further?",
      "answer" : "Please ensure that the photo you are attempting to upload meets the defined parameters. If it does, please verify that your internet connection is functioning properly. If you continue to experience difficulties, kindly report this issue via email to admissions@sst.scaler.com. "
   
   },

   {
      "question" : "I cleared the NSET but did not receive calendar invite for the PI (personal interview). What do I do?",
      "answer" : "Please monitor your registered email inbox for details regarding the Personal Interview, as well as check the calendar for the scheduled PI time. If you are still unable to find the link, please reach out to admissions_sst@scaler.com or call our customer support team. Kindly be informed that we are unable to accommodate any changes to the date or time under any circumstances."
   
   },
   {
      "question" : "Did not receive PI link. What do I do?",
      "answer" : "Please monitor your registered email inbox for details regarding the Personal Interview, as well as check the calendar for the scheduled PI time. If you are still unable to find the link, please reach out to admissions_sst@scaler.com or call our customer support team. Kindly be informed that we are unable to accommodate any changes to the date or time under any circumstances."
   
   },
   {
  "question": "How do I get admission to Scaler School of Technology?",
  "answer": "To know more about the admissions process, please watch this video: https://www.youtube.com/watch?v=_Vr_kjjaROw&t=68s\n\nThe application process for Scaler School of Technology consists of three essential steps:\n\n**Step 1:** Complete the application form by providing all necessary details accurately. This helps us understand your background and qualifications.\n\n**Step 2:** Attempt the NSET (Scaler's entrance test) with full dedication. This test evaluates your skills and potential in tech-related areas.\n\n**Step 3:** If you clear the NSET, you'll move to the personal interview round. This is a face-to-face interaction where we assess your goals, motivation, and fit for the program.\n\nAdmission offers are based on strong performance in both the NSET and the interview. We're looking for candidates with exceptional potential and a true passion for technology."
}
,

   {
      "question" : "How can I get a admission counsellor?",
      "answer" : "To learn more about Scaler School of Technology and have all your questions answered, join us in our weekly Q&A sessions where we address all your concerns and doubts. Register for free sessions here: https://www.scaler.com/school-of-technology/events"
   
   },
   {
      "question" : "Can I get any contact number for more information?",
      "answer" : "To learn more about Scaler School of Technology and have all your questions answered, join us in our weekly Q&A sessions where we address all your concerns and doubts. Register for free sessions here: https://www.scaler.com/school-of-technology/events"
   
   },
   {
  "question": "How many scholarships are available at Scaler School of Technology?",
  "answer": "There are broadly two types of scholarships available:\n\n1. **Merit-Based Scholarships** – For students with exceptional academic and extracurricular achievements.\n2. **Need-Based Scholarships** – For students from financially challenged backgrounds (family income less than ₹5 LPA).\n\nAll scholarships are awarded by the **Scaler Impact Foundation**, supported by leaders like Vijay Shekhar Sharma (Founder & CEO, Paytm) and Prasanna Sankar (Founder, Rippling).\n\nSince the number of scholarships is limited, early application is highly recommended to improve your chances.\n\n**Steps to Apply for a Scholarship:**\n✅ **Step 1:** Register for NSET on the Scaler School of Technology website: https://www.scaler.com/school-of-technology/application/\n✅ **Step 2:** Complete the profile form with academic scores (Class X, XII, JEE, BITSAT) and extracurriculars. For need-based applications, submit family income details.\n✅ **Step 3:** Upload supporting documents (e.g., previous school fee slip) for financial verification if applying for need-based scholarship."
}
,


   {
      "question" : " When is the last day for applying for the NSET?",
      "answer" : "To know more about important dates and deadlines for the admissions cycle, please visit: https://www.scaler.com/school-of-technology/admission/#timeline"
   
   },
   {
      "question" : "Instead of math I have taken statistics as a subject. Can I apply for UG CS degree at SST?",
      "answer" : "No, you can not apply at Scaler School of Technology in such a case as it is mandetory score above 60% in Mathematics to be eligible for the course."
   
   },
   {
      "question" : "Which board students are eligible to apply for this UG program at Scaler School of Technology?",
      "answer" : "Students from all boards are eligible to apply at Scaler School of Technology. The Scaler School of Technology welcomes students who have completed their Class XII exams in 2025 or earlier irrespective of their passing board, provided they are under the age of 20. This age limit allows us to focus on delivering a tailored educational experience for young individuals who are at a critical stage in their academic journey.To apply for the program at Scaler School of Technology, please visit our official website at:  https://www.scaler.com/school-of-technology/"
   
   },
   {
      "question" : "Can I apply for SST if I come from a commerce background?",
      "answer" : "Yes, we welcome students from all backgrounds. However, admission offers are contingent upon having mathematics as a subject in XII and achieving a mathematics score of above 60%, along with passing XII finals. Students will not be eligible for a refund if found ineligible. Ensure to provide all necessary information and documentation required during the application process."
   
   },
   {
  "question": "I have participated in a global olympiad. Can I mention this during my personal interview round?",
  "answer": "Yes, absolutely! You can upload your achievements with proof in the 'Achievements' section of the Interview Profiling Form.\n\nWe’re excited to announce the inclusion of profile-based shortlisting alongside NSET. As part of the selection criteria, we consider one or more of the following:\n\n1⃣ Outstanding academic performance in Classes X and XII, especially in Mathematics\n2⃣ High percentile in competitive exams\n3⃣ Notable achievements in tech competitions like IOI, CodeChef, and hackathons\n\nThese criteria help us recognize and reward candidates with strong potential across diverse academic and technical domains."
}
,
{
  "question": "Do we need to fill the interview profiling form before giving the NSET test?",
  "answer": "While it is not mandatory to fill the interview profiling form before taking the NSET test, it is highly recommended. Completing it early helps with profile-based shortlisting, which is now considered alongside NSET performance.\n\nCandidates who pass the written test are encouraged to fill out the profiling form promptly, as it will be closed once interviews are scheduled.\n\nAs part of the selection criteria, Scaler considers:\n1⃣ Outstanding academic performance in X and XII, especially in Mathematics\n2⃣ High percentile in competitive exams\n3⃣ Notable achievements in tech competitions like IOI, CodeChef, and hackathons\n\nThese factors help us identify and reward students with strong academic and technical potential."
},

   {
      "question" : "How to change email address? ",
      "answer" : "You cannot alter the email address provided in your application; however, you can change your account email through the 'My Profile' section. Within this section, there is an option specifically designated for changing your email address."
   
   },
   {
      "question" : "What should I do if I don't have a surname?",
      "answer" : "You can simply leave the surname field blank"
   
   },
   {
      "question" : " I  am not receiving any replies to my email. What should I do?",
      "answer" : "Please wait for some time; we will definitely reply to your email."
   
   },
   {
      "question" : "I currently don't have an income  certificate. What should I do?",
      "answer" : "You will need to arrange for the income certificate before your interviews are scheduled. Failure to do so will result in your disqualification from consideration for our scholarships"
   
   },
   {
      "question" : "I have filled out the interview form, but it still isn't showing the green mark. What should I do?",
      "answer" : "The green tick may not appear because the form remains active until the interviews are scheduled, even after you have filled it out. We allow applicants to refill the form if they need to update any documents or results further."
   
   },
   {
      "question" : "Where are the centres located for the of NSET?",
      "answer" : "The Scaler NSET is an online exam. It is conducted in an online mode and follows a proctored setup. This means that the exam is administered remotely from the convinience of your home or any other location of your choice. If you do not have access to a personal laptop, you may take the test from a cyber cafe or any other suitable location. The exam is conducted in a completely proctored setup to ensure a fair and secure testing environment. Giving the test from mobile is not allowed & the laptop/pc should have a working camera. "
   
   },
   {
      "question" : "Is the NSET exam written or online?",
      "answer" : "The Scaler NSET is an online exam. It is conducted in an online mode and follows a proctored setup. This means that the exam is administered remotely from the convinience of your home or any other location of your choice. If you do not have access to a personal laptop, you may take the test from a cyber cafe or any other suitable location. The exam is conducted in a completely proctored setup to ensure a fair and secure testing environment. Giving the test from mobile is not allowed & the laptop/pc should have a working camera."
   
   },
   {
      "question" : "How much marks do I need to clear the test?",
      "answer" : "The passing marks for the Scaler NSET may vary depending on the level of competition. The NSET Prep toolkit provided to you upon completing your application includes comprehensive information on the marks distribution for each section. It is essential to utilize these resources to better prepare yourself for the exam and perform at your best during the Scaler NSET. You should refer to the selection criteria for the NSET."
   
   },
   {
      "question" : "If i fail all 3 NSET attempts this year can i still attempt next year? ",
      "answer" : "Yes you can but if you you are twenty years or younger and have completed your 12th grade education, with a score of more than 60% in Mathematics for their twelfth grade examination."
   
   },
   {
  "question": "What does a day look like for a student at Scaler School of Technology (SST)?",
  "answer": "At Scaler School of Technology, each day is designed to foster learning, growth, and well-being. Here's what a typical day looks like:\n\n**Morning Routine:** The day begins with a healthy breakfast as students arrive at the macro campus by 9 AM.\n\n**Lectures and Modules:** Students attend engaging lectures covering two different modules, ensuring a varied and enriching academic experience.\n\n**Lab Sessions and Assignments:** Post-lectures, students engage in lab sessions and complete assignments to apply theoretical knowledge in practical ways.\n\n**Academic Support:** Instructors and Batch Success Managers provide continuous guidance, helping students overcome academic challenges and enhance their learning.\n\n**Well-being:** Students have access to an on-campus gym and regular mental wellness check-ins, thanks to partnerships like Lissun. On-campus counselors are also available to ensure sound mental health.\n\n**Cultural Celebrations:** Festivals like Diwali and Independence Day are celebrated with enthusiasm, building a strong community atmosphere.\n\n**Social and Culinary Life:** The micro campus offers affordable and diverse dining options, creating spaces for students to relax and socialize after classes."
}
,
{
  "question": "Tell me more about the first batch at Scaler School of Technology",
  "answer": "The first batch at Scaler School of Technology is a highly competitive and accomplished cohort, selected from over 54,000 applications with an acceptance rate of just 3.8%.\n\n🔹 **Top Talent**: Over 60 students left premier institutions like IITs and global universities to join SST.\n🔹 **Diverse Backgrounds**: Students represent 25+ states and bring achievements from various academic and extracurricular domains.\n🔹 **Coding Journey**: 65% of students were beginners in coding, yet have rapidly progressed to participate in elite competitions like ICPC and build impactful tech solutions.\n🔹 **Clubs & Projects**: Active in student clubs and initiatives, they've contributed to high-impact projects such as the Bhashini Project, recognized by the Prime Minister of India.\n\n👥 **Meet the Students**: You can explore the journeys of first batch students here: https://sst-student-directory.notion.site/77edf959308d4c0685a2290f487ce48c?v=42554cbca23b4b72b571eae84586306b\n\n🎥 **Watch Their Story**: https://youtu.be/10JMuMJ6U48?si=66Xei9RiMWtRoQoT"
}
,

   {
       "question" :"How many Personal Interviews can I give?",
       "answer" : "You can retake the NSET up to 3 times and can attempt the personal interview round 2 times in an academic year post qualifying the NSET round. For detailed information regarding the test dates and other important details, please visit our admissions page at: https://www.scaler.com/school-of-technology/admission/"
   },
   {
       "question" :"How much is the retake fees for NSET?",
       "answer" : "Students can retake the NSET three times in an admission cycle at a cost of Rs. 100 only per re-attempt."
   },
   {
       "question" :"Is SST recognized by any governing education bodies?",
       "answer" : "Yes. The Scaler School of Technology (SST) program is approved by the National Skill Development Corporation (NSDC), a government-backed body under the Ministry of Skill Development and Entrepreneurship. NSDC approval affirms the program’s alignment with national skill-building priorities and its focus on industry-relevant, outcome-driven education.\n To ensure our students also receive a UGC-recognized degree, we recommend they parallelly enroll in a degree program offered by either IIT Madras or BITS Pilani. This dual approach allows students to benefit from SST’s cutting-edge curriculum while also meeting degree-related eligibility criteria for opportunities like postgraduate admissions or civil services."
   },
   {
    "question": "Does one need basic knowledge of computer and programming to appear for the NSET exam or to join Scaler School of Technology?",
    "answer": "No, basic knowledge of computer programming is not required to appear for the NSET exam or to join Scaler School of Technology. In fact, 65% of students admitted to SST had no prior coding knowledge when they joined. Admission is based on aptitude, profile, and interest in learning computer science. The exam and curriculum are designed to accommodate learners at all levels.\n\nWithin nine months, students progress from beginners to independently building impressive projects and participating in competitions like ICPC and developing apps for the Government of India.\n\nIf you are interested in computer science, we encourage you to take the Scaler NSET. Learn more here: https://youtu.be/_Vr_kjjaROw?feature=shared"
  },
  {
    "question": "Why should I apply early for the 2025 intake of Scaler School of Technology?",
    "answer": "Applying early offers several benefits:\n\n1. **Higher chances for scholarships** — Early applicants are twice as likely to secure scholarships.\n2. **Flexible exam slots** — Choose from any of the 5 open slots available until April, allowing you to plan according to your schedule. Check open slots here: https://www.scaler.com/school-of-technology/admission/#timeline\n3. **Multiple attempts for success** — Apply early to get up to 3 attempts at the exam, increasing your chances to improve and succeed."
  },
   {
       "question" :"What specializations can students choose from?",
       "answer" : "Students at SST can specialize in one of the following tracks: Software Development, Artificial Intelligence & Machine Learning, Blockchain & Cybersecurity, or Algorithmic Trading. Each track includes advanced projects and in-depth coursework tailored to industry needs. For more information on the specilizations, check our website here: https://www.scaler.com/school-of-technology/#:~:text=Phase%203%3A%20Specialize,for%20the%20industry"
   },
   {
       "question" :"What events and competitions are held on campus?",
       "answer" : "SST hosts a variety of events, including hackathons, coding competitions, cultural festivals, tech expos, and super-mentor sessions by industry leaders. These events provide students with opportunities to learn, compete, and network."
   },
   {
       "question" :"How accessible is the campus via public transport?",
       "answer" : "The SST campus is located in Bangalore, a hub of tech innovation, and is well-connected by public transport, including buses, metro services, and other local transit options, ensuring easy accessibility for students."
   },
   {
       "question" :"Can a Polytechnic/Diploma student apply for SST?",
       "answer" : "Yes, Polytechnic or Diploma students are eligible to apply for SST, provided they meet the admission criteria and have scored more than 60 marks in Mathematics. They must also clear the National Scaler Entrance Test (NSET).Please note that the student would have to start from the first year again."
   },
   {
       "question" :"Scholarship opportunities for international students: How can they apply for them?",
       "answer" : "Currently only Nepal students are eligible to apply for our programmes.They can apply for scholarships by submitting an application during the admission process. Details regarding available scholarships, eligibility criteria, and application procedures will be shared with applicants once they initiate the admission process."
   },
   {
       "question" :" What is the Cut-off of NSET exam",
       "answer" : " The cut-off for the National Scaler Entrance Test (NSET) is dynamic and depends on the number of applicants and their performance. Typically, the top 10 percentile of candidates from each exam are selected for admission. Specific details are shared during the admission process."
   },
   {
       "question" :"What are the safety measures taken for female students?",
       "answer" : "SST prioritizes the safety and well-being of female students with several robust measures. The female hostel section is secured with biometric access, ensuring that only authorized individuals can enter. Even male relatives, including the student’s father, are not permitted inside the female section. A dedicated female warden and security guard are available 24/7 to provide support and maintain safety. Additionally, the campus enforces a strict zero- tolerance policy towards harassment, supported by grievance redressal mechanisms and continuous monitoring through CCTV cameras."
   },
   {
       "question" :"How to travel between campuses?",
       "answer" : "SST provides a shuttle bus service for easy travel between campuses. However, students often prefer alternatives such as walking, using Yulu bikes, or taking auto-rickshaws, as the distance is only 1 to 1.5 km."
   },
   {
       "question" :"What are the food options available in the hostel?",
       "answer" : "The hostel offers a well-balanced menu with vegetarian and non-vegetarian options, catering to various dietary preferences. Meals are prepared in a hygienic environment to ensure quality and variety for students."
   },
   {
       "question" :"Are electrical appliances allowed in the hostel?",
       "answer" : "No personal electrical appliances like irons, kettles, or induction stoves are allowed in the hostel rooms for safety reasons. However, common areas are equipped with necessary appliances like microwave ovens, induction cookers, water dispensers and ironing stations."
   },
   {
       "question" :"Are male and female hostels separate or the same?",
       "answer" : "Male and female hostels are completely separate, with distinct access controls and dedicated staff to ensure privacy and safety."
   },
   {
       "question" :"What facilities are available in the hostel?",
       "answer" : "The hostel offers several amenities, including laundry services, a common TV lounge, high-speed internet, study rooms, and recreational areas. Additionally, each floor has a pantry for basic food preparation."
   },
   {
       "question" :"What all items do I need to purchase before coming to the hostel?",
       "answer" : "Students are required to bring their own bedsheets, mattress, pillow, bucket, mug, locks, and other personal essentials. A detailed checklist is usually shared before the commencement of the session to help students prepare adequately."
   },

   {
       "question" : " I’m repeatedly redirected to the login page during the Scaler NSET exam or the personal interview round. What should I do?",
       "answer":"f you're being redirected to the login page, try clearing your browser's cache and cookies. Additionally, you can open an incognito or private browsing window and ensure you're using a supported browser, such as Google Chrome. This should resolve the issue."
   },
    {
       "question" : "I haven't received the OTP to log in. What should I do?",
       "answer":"First, verify that you've entered the correct registered email or phone number. If you're still facing issues, please reach out to our support team at admissions_sst@scaler.com for further assistance."
   },
    {
  "question": "The test platform for Scaler NSET/Personal interview round is asking for camera permission again, even though I already granted it. What should I do?",
  "answer": "If the platform is repeatedly asking for camera permission, try the following steps:\n\n• Check your browser settings to ensure the platform URL has camera permissions enabled.\n• Restart your browser and log in again.\n• Make sure you are using the latest version of your browser.\n• If the issue continues, try using another laptop or PC that has a working camera.\n• If none of these solutions work, please contact support for further assistance."
}
,
    {
       "question" : "I cannot enable camera permissions on my device. Can I use another device for the NSET exam/Personal Interview round?",
       "answer":"Yes, you're welcome to use a different laptop or PC with a functional camera. Just ensure the new device meets the system requirements. Please note that mobile phones and tablets are not supported for the exam."
   },
    {
       "question" : "My system shut down unexpectedly during the NSET test or Personal Interview rouund. Can I continue from another device?",
       "answer":"Yes, you can resume the test on a different laptop or PC. You'll need to log in with the session link provided to you. Make sure the new device is compatible and has a working camera."
   },
    {
  "question": "The 'End Test' button on Scaler NSET platform isn’t working, even though I’ve clicked it. What should I do?",
  "answer": "If the 'End Test' button is not responding, try the following:\n\n• Wait a few seconds and click the button again.\n• Refresh your browser, log in again, and resume your test session.\n• If the issue still persists, contact support immediately at admissions_sst@scaler.com."
}
,
   {
       "question" : "I experienced technical issues during the Scaler NSET test. Were my responses saved?",
       "answer":"Our platform auto-saves your responses periodically. However, if you faced issues, please reach out to support to verify whether your responses were successfully submitted. "
   },
    {
       "question" : "I had limited time left after resolving technical issues that came in while the NSET exam. Can I retake the test",
       "answer":" you experience verified technical issues, you can request a reschedule of your test. Please contact support with a detailed explanation and any relevant screenshots or recordings to support your request"
   },
    {
       "question" : "Do I need to use the same device for the sample test and the NSET exam?",
       "answer":"While it’s best to use the same device for consistency, you can use a different laptop or PC if necessary. Ensure that the device has a working camera and meets the system requirements."
   },
    {
       "question" : "Can I take the NSET exam on a mobile phone or tablet?",
       "answer":"No, the NSET exam can only be taken on a laptop or PC with a functional camera. Mobile phones and tablets are not supported."
   },
    {
       "question" : "I encountered technical issues during the NSET. Can I retake the test?",
       "answer":"Yes, if you're facing verified technical issues, you can request a retake without any additional charges. Please contact support to submit your request."
   },
    {
       "question" : "Where can I find the NSET exam link?",
       "answer":"The exam link will be shared via email. If you can't find it in your inbox, please check your spam or junk folder. If you're still unable to locate the link, feel free to contact support for assistance."
   },
   {
       "question" : "What should I do if I'm still experiencing issues in attempting the  SET exam despite following all the troubleshooting steps?",
       "answer":"Please reach out to customer support immediately. It’s helpful to provide screenshots, error messages, or recordings of the issue, which will assist the team in resolving the problem more effectively. If the issue remains unresolved, you can request alternative solutions from the support team. Connect with the support team here: admissions_sst@scaler.com "
   },


]

def search_answer(user_question):
    best_match = None
    highest_score = 0
    for pair in qa_pairs:
        score = fuzz.token_set_ratio(user_question.lower(), pair["question"].lower())
        if score > highest_score:
            highest_score = score
            best_match = pair
    if highest_score > 60:
        return best_match["answer"]
    else:
        return "Sorry, I couldn’t find the answer to that question."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi! Ask me any question related to SST admissions.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text
    answer = search_answer(user_question)
    await update.message.reply_text(answer)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
