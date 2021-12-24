from flask import Flask, render_template, request
import pickle
import numpy as np

# Load the Random Forest CLassifier model
filename = 'first-innings-score-lr-model.pkl'
regressor = pickle.load(open(filename, 'rb'))

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/meetus')
def meet():
    return render_template('meet.html')
@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/predict', methods=['POST'])
def predict():
    temp_array = list()

    if request.method == 'POST':


        batting_team = request.form['batting-team']
        team_encoding = {'Mumbai Indians': 1,
                         'Royal Challengers Bangalore': 2,
                         'Kolkata Knight Riders': 3,
                         'Kings XI Punjab': 4,
                         'Chennai Super Kings': 5,
                         'Rajasthan Royals': 6,
                         'Delhi Daredevils': 7,
                         'Sunrisers Hyderabad': 8,
                         'Deccan Chargers': 9,
                         'Pune Warriors': 10,
                         'Delhi Capitals': 11,
                         'Gujarat Lions': 12,
                         'Rising Pune Supergiants': 13,
                         'Rising Pune Supergiant': 13,
                         'Kochi Tuskers Kerala': 14}
        bat_team=team_encoding.get(batting_team)

        bowling_team = request.form['bowling-team']
        bowl_team = team_encoding.get(bowling_team)

        venue=request.form['Venue']

        venue1=['Arun Jaitley Stadium','Barabati Stadium','Brabourne Stadium',
     'Buffalo Park', 'De Beers Diamond Oval' ,'Dr DY Patil Sports Academy',
     'Dr. Y.S. Rajasekhara Reddy ACA-VDCA Cricket Stadium',
     'Dubai International Cricket Stadium' ,'Eden Gardens', 'Feroz Shah Kotla',
     'Green Park', 'Himachal Pradesh Cricket Association Stadium',
     'Holkar Cricket Stadium', 'JSCA International Stadium Complex', 'Kingsmead',
     'M Chinnaswamy Stadium', 'M.Chinnaswamy Stadium', 'MA Chidambaram Stadium',
     'MA Chidambaram Stadium, Chepauk',
     'MA Chidambaram Stadium, Chepauk, Chennai',
     'Maharashtra Cricket Association Stadium' ,'Nehru Stadium',
     'New Wanderers Stadium' ,'Newlands' ,'OUTsurance Oval',
     'Punjab Cricket Association IS Bindra Stadium',
     'Punjab Cricket Association IS Bindra Stadium, Mohali',
     'Punjab Cricket Association Stadium, Mohali',
     'Rajiv Gandhi International Stadium',
     'Rajiv Gandhi International Stadium, Uppal',
     'Sardar Patel Stadium, Motera' ,'Saurashtra Cricket Association Stadium',
     'Sawai Mansingh Stadium',
     'Shaheed Veer Narayan Singh International Stadium',
     'Sharjah Cricket Stadium' ,'Sheikh Zayed Stadium', "St George's Park",
     'Subrata Roy Sahara Stadium' ,'SuperSport Park',
     'Vidarbha Cricket Association Stadium, Jamtha' ,'Wankhede Stadium',
     'Wankhede Stadium, Mumbai']
        venue_add=999

        for i in range(len(venue1)):
            if (venue1[i] == venue):
                venue_add = i


        batsman = request.form['Batsman']
        bowler = request.form['Bowler']
        batsman_list=['A Ashish Reddy', 'A Chopra', 'A Flintoff', 'A Mishra', 'A Mukund',
         'A Symonds' ,'AA Bilakhia', 'AA Jhunjhunwala', 'AB Agarkar' ,'AB Barath',
         'AB McDonald' ,'AB de Villiers' ,'AC Blizzard' ,'AC Gilchrist', 'AC Voges',
         'AD Hales' ,'AD Mascarenhas', 'AD Mathews' ,'AD Nath', 'AD Russell',
         'AG Paunikar' ,'AJ Finch', 'AL Menaria', 'AM Nayar', 'AM Rahane' ,'AN Ghosh',
         'AP Majumdar' ,'AP Tare', 'AR Patel', 'AS Raut', 'AT Rayudu', 'AUK Pathan',
         'Anirudh Singh' ,'Ankit Sharma' ,'Azhar Mahmood', 'B Chipli', 'BA Stokes',
         'BB McCullum' ,'BB Samantray' ,'BJ Haddin' ,'BJ Hodge' ,'BMAJ Mendis',
         'BR Dunk', 'C Madan', 'C Munro' ,'C de Grandhomme', 'CA Ingram', 'CA Lynn',
         'CA Pujara' ,'CH Gayle' ,'CH Morris', 'CJ Anderson' ,'CJ Ferguson', 'CL White'
         'CM Gautam' ,'D Padikkal' ,'DA Miller', 'DA Warner', 'DB Das' ,'DB Ravi Teja',
         'DJ Bravo' ,'DJ Harris' ,'DJ Hooda', 'DJ Hussey', 'DJ Jacobs' ,'DJ Thornely',
         'DJG Sammy' ,'DJM Short' ,'DPMD Jayawardene', 'DR Martyn' ,'DR Smith',
         'DS Lehmann' ,'DT Christian' ,'E Lewis' ,'EJG Morgan', 'ER Dwivedi',
         'F du Plessis', 'FY Fazal', 'G Gambhir' ,'GC Smith', 'GH Vihari' ,'GJ Bailey',
         'GJ Maxwell' ,'Gurkeerat Singh' ,'H Klaasen' ,'HH Gibbs' ,'HH Pandya',
         'HM Amla', 'Harbhajan Singh', 'IK Pathan', 'IR Jaggi' ,'Ishan Kishan',
         'J Arunkumar' ,'J Botha' ,'JA Morkel' ,'JC Archer', 'JC Buttler' ,'JD Ryder',
         'JEC Franklin' ,'JH Kallis', 'JJ Roy' ,'JL Denly' ,'JM Bairstow', 'JM Kemp',
         'JO Holder' ,'JP Duminy' ,'JP Faulkner', 'JR Hopes' ,'JR Philippe' ,'K Goel',
         'K Gowtham' ,'K Rabada' ,'KA Pollard', 'KC Sangakkara' ,'KD Karthik',
         'KH Pandya' ,'KK Cooper' ,'KK Nair' ,'KL Rahul' ,'KM Jadhav' ,'KP Pietersen',
         'KS Williamson', 'KV Sharma' ,'Kamran Akmal', 'L Ronchi' ,'LA Carseldine',
         'LA Pomersbach' ,'LJ Wright' ,'LMP Simmons' ,'LPC Silva', 'LR Shukla',
         'LRPL Taylor' ,'LS Livingstone' ,'M Kaif' ,'M Klinger', 'M Manhas', 'M Rawat',
         'M Vijay' ,'M Vohra' ,'MA Agarwal' ,'MC Henriques' ,'MC Juneja' ,'MD Mishra',
         'MDKJ Perera' ,'MEK Hussey', 'MJ Clarke', 'MJ Guptill', 'MJ Lumb',
         'MJ McClenaghan' ,'MK Lomror' ,'MK Pandey', 'MK Tiwary' ,'ML Hayden' ,'MM Ali',
         'MN Samuels' ,'MN van Wyk' ,'MP Stoinis', 'MS Bisla', 'MS Dhoni', 'MS Wade',
         'MV Boucher' ,'Mandeep Singh' ,'Misbah-ul-Haq', 'Mohammad Ashraful',
         'Mohammad Hafeez', 'N Jagadeesan' ,'N Pooran' ,'N Rana', 'N Saini',
         'NJ Maddinson' ,'NLTC Perera' ,'NS Naik' ,'NV Ojha' ,'Niraj Patel', 'OA Shah',
         'P Kumar' ,'P Negi' ,'P Simran Singh', 'PA Patel', 'PA Reddy' ,'PC Valthaty',
         'PD Collingwood' ,'PJ Cummins' ,'PK Garg' ,'PP Chawla' ,'PP Shaw', 'PR Shah',
         'Q de Kock' ,'R Ashwin' ,'R Bishnoi', 'R Dravid','Rohit Sharma', 'R McLaren', 'R Parag',
         'R Sathish', 'R Tewatia' ,'RA Jadeja' ,'RA Tripathi', 'RD Gaikwad' ,'RE Levi',
         'RE van der Merwe' ,'RG Sharma' ,'RJ Quiney', 'RK Bhui', 'RM Patidar',
         'RN ten Doeschate', 'RR Pant' ,'RR Rossouw' ,'RR Sarwan' ,'RS Bopara',
         'RT Ponting' ,'RV Gomez', 'RV Uthappa', 'S Anirudha', 'S Badrinath',
         'S Chanderpaul', 'S Dhawan', 'S Gopal', 'S Rana', 'S Sohal', 'S Sriram',
         'S Vidyut', 'SA Asnodkar' ,'SA Yadav' ,'SB Styris' ,'SC Ganguly' ,'SD Chitnis',
         'SD Lad', 'SE Marsh' ,'SK Raina' ,'SM Curran' ,'SM Katich', 'SM Pollock',
         'SN Khan' ,'SO Hetmyer', 'SP Fleming' ,'SP Goswami' ,'SP Jackson' ,'SP Narine',
         'SPD Smith' ,'SR Tendulkar' ,'SR Watson', 'SS Iyer' ,'SS Tiwary',
         'ST Jayasuriya' ,'STR Binny', 'SV Samson' ,'SW Billings' ,'Sachin Baby',
         'Salman Butt' ,'Shahid Afridi' ,'Shakib Al Hasan' ,'Shoaib Malik'
         'Shubman Gill' ,'Sohail Tanvir' ,'Sunny Singh' ,'T Banton', 'T Henderson',
         'T Kohli', 'TD Paine', 'TL Suman' ,'TM Dilshan', 'TM Head' ,'UA Birla',
         'UBT Chand' ,'UT Khawaja', 'V Kohli' ,'V Sehwag' ,'V Shankar', 'VH Zol',
         'VVS Laxman', 'Vishnu Vinod' ,'W Jaffer' ,'WD Parnell' ,'WP Saha',
         'Washington Sundar' ,'Y Gnaneswara Rao' ,'Y Nagar' ,'Y Venugopal Rao',
         'YBK Jaiswal' ,'YK Pathan', 'YV Takawale' ,'Yashpal Singh' ,'Younis Khan',
         'Yuvraj Singh', 'Z Khan']
        batsman_add=999
        for i in range(len(batsman_list)):
            if (batsman_list[i] == batsman):
                batsman_add= i
        bowler_list=['A Ashish Reddy', 'A Chandila', 'A Choudhary', 'A Dananjaya' ,'A Flintoff',
 'A Kumble' ,'A Mishra' ,'A Mithun' ,'A Nehra', 'A Nel' ,'A Nortje' ,'A Singh',
 'A Symonds' ,'A Uniyal', 'A Zampa', 'AA Chavan', 'AA Jhunjhunwala',
 'AA Noffke' ,'AB Agarkar', 'AB Dinda' ,'AB McDonald', 'AC Thomas' ,'AC Voges',
 'AD Mascarenhas', 'AD Mathews' ,'AD Russell', 'AF Milne','AG Murtaza',
 'AJ Finch' ,'AJ Tye', 'AL Menaria' ,'AM Nayar' ,'AM Salvi' ,'AN Ahmed',
 'AP Dole' ,'AR Patel' ,'AS Joseph', 'AS Rajpoot', 'Anand Rajan',
 'Ankit Sharma' ,'Ankit Soni' ,'Anureet Singh' ,'Arshdeep Singh', 'Avesh Khan',
 'Azhar Mahmood', 'B Akhil', 'B Geeves', 'B Kumar' ,'B Laughlin', 'B Lee',
 'B Stanlake' ,'BA Bhatt' ,'BA Stokes' ,'BAW Mendis' ,'BB Sran' ,'BCJ Cutting'
 'BE Hendricks', 'BJ Hodge' ,'BW Hilfenhaus' ,'Basil Thampi', 'Bipul Sharma',
 'C de Grandhomme' ,'CH Gayle' ,'CH Morris', 'CJ Anderson' ,'CJ Dala',
 'CJ Green' ,'CJ Jordan' ,'CJ McKay' ,'CK Langeveldt', 'CR Brathwaite',
 'CR Woakes', 'CRD Fernando' ,'CV Varun' ,'D Wiese' ,'D du Preez',
 'DAJ Bracewell', 'DE Bollinger', 'DJ Bravo', 'DJ Hooda', 'DJ Hussey',
 'DJ Muthuswami', 'DJ Willey' ,'DJG Sammy', 'DL Chahar' ,'DL Vettori',
 'DNT Zoysa', 'DP Nannes' ,'DP Vijaykumar', 'DR Sams', 'DR Smith',
 'DS Kulkarni' ,'DT Christian' ,'DW Steyn', 'FH Edwards', 'GB Hogg',
 'GC Viljoen' ,'GD McGrath' ,'GH Vihari', 'GJ Maxwell', 'GR Napier',
 'GS Sandhu' ,'Gagandeep Singh' ,'Gurkeerat Singh' ,'HF Gurney', 'Hardik Pandya',
 'HV Patel' ,'Harbhajan Singh' ,'Harmeet Singh', 'Harmeet Singh (2)',
 'Harpreet Brar', 'I Sharma', 'I Udana', 'IC Pandey', 'IK Pathan', 'IS Sodhi',
 'Imran Tahir', 'Iqbal Abdulla' ,'J Botha', 'J Suchith', 'J Syed Mohammad',
 'J Theron' ,'J Yadav', 'JA Morkel' ,'JC Archer', 'JD Ryder' ,'JD Unadkat'
 'JDP Oram' ,'JDS Neesham' ,'JE Taylor', 'JEC Franklin' ,'JH Kallis',
 'JJ Bumrah', 'JJ van der Wath', 'JL Pattinson' ,'JO Holder' ,'JP Behrendorff',
 'JP Duminy' ,'JP Faulkner' ,'JPR Scantlebury-Searles', 'JR Hazlewood',
 'JR Hopes', 'JW Hastings', 'Jaskaran Singh', 'Joginder Sharma' ,'K Gowtham',
 'K Khejroliya' ,'K Rabada' ,'K Santokie' ,'K Upadhyay' ,'KA Jamieson',
 'KA Pollard' ,'KAJ Roach', 'KC Cariappa', 'Kunal Pandya' ,'KJ Abbott' ,'KK Ahmed',
 'KK Cooper' ,'KL Nagarkoti' ,'KM Asif' ,'KMA Paul' ,'KMDN Kulasekara',
 'KP Appanna' ,'KP Pietersen' ,'KS Williamson', 'KV Sharma' ,'KW Richardson',
 'Kamran Khan' ,'Karanveer Singh', 'Kartik Tyagi' ,'Kuldeep Yadav', 'L Ablish'
 'L Balaji' ,'L Ngidi' ,'LA Carseldine', 'LE Plunkett', 'LH Ferguson',
 'LJ Wright' ,'LR Shukla', 'M Ashwin', 'M Jansen' ,'M Kartik', 'M Morkel',
 'M Muralitharan', 'M Ntini', 'M Prasidh Krishna' ,'M Vijay', 'M de Lange',
 'MA Starc' ,'MB Parmar', 'MC Henriques' ,'MF Maharoof' ,'MG Johnson'
 'MG Neser' ,'MJ Henry', 'MJ McClenaghan' ,'MJ Santner' ,'MM Ali' ,'MM Patel',
 'MM Sharma' ,'MN Samuels', 'MP Stoinis' ,'MR Marsh' ,'MS Gony'
 'Mashrafe Mortaza' ,'Mohammad Asif', 'Mohammad Nabi' ,'Mohammed Shami',
 'Mohammed Siraj' ,'Monu Kumar' ,'Mujeeb Ur Rahman' ,'Mustafizur Rahman'
 'N Rana', 'NA Saini' ,'NB Singh', 'ND Doshi' ,'NJ Rimmington', 'NL McCullum',
 'NLTC Perera' ,'NM Coulter-Nile', 'O Thomas', 'P Amarnath', 'P Awana'
 'P Kumar', 'P Negi' ,'P Parameswaran', 'P Sahu' ,'P Suyal', 'PJ Cummins',
 'PJ Sangwan', 'PM Sarvesh Kumar' ,'PP Chawla' ,'PP Ojha' ,'PV Tambe',
 'Pankaj Singh', 'Parvez Rasool', 'R Ashwin', 'R Bhatia' ,'R Dhawan',
 'R McLaren' ,'R Parag' ,'R Rampaul', 'R Sharma' ,'R Shukla', 'R Tewatia',
 'R Vinay Kumar', 'RA Jadeja' ,'RA Shaikh' ,'RD Chahar', 'RE van der Merwe',
 'RG More' ,'RG Sharma', 'RJ Harris' ,'RJ Peterson', 'RP Singh', 'RR Bhatkal',
 'RR Bose' ,'RR Powar' ,'RR Raje' ,'RW Price', 'Rashid Khan', 'Rasikh Salam',
 'Ravi Bishnoi' ,'S Aravind', 'S Badree' ,'S Dhawan' ,'S Gopal', 'S Kaul',
 'S Kaushik' ,'S Ladda' ,'S Lamichhane' ,'S Nadeem', 'S Narwal', 'S Randiv',
 'S Sandeep Warrier' ,'S Sreesanth', 'S Tyagi' ,'SA Abbott' ,'SA Yadav',
 'SB Bangar' ,'SB Jakati', 'SB Styris' ,'SB Wagh' ,'SC Ganguly',
 'SC Kuggeleijn' ,'SD Chitnis' ,'SE Bond' ,'SJ Srivastava', 'SK Raina',
 'SK Trivedi', 'SK Warne' ,'SL Malinga', 'SM Boland' ,'SM Curran', 'SM Harwood',
 'SM Pollock', 'SMSM Senanayake' ,'SN Thakur' ,'SP Narine', 'SR Watson',
 'SS Agarwal' ,'SS Cottrell', 'SS Mundhe' ,'SS Sarkar' ,'ST Jayasuriya',
 'STR Binny' ,'SW Tait' ,'Sandeep Sharma' ,'Shahid Afridi' ,'Shakib Al Hasan',
 'Shivam Mavi' ,'Shoaib Ahmed' ,'Shoaib Akhtar' ,'Sohail Tanvir',
 'Sunny Gupta' ,'T Natarajan', 'T Thushara' ,'TA Boult', 'TG Southee',
 'TK Curran' ,'TL Suman' ,'TM Dilshan' ,'TP Sudhindra' ,'TS Mills',
 'TU Deshpande' ,'Tejas Baroka' ,'UT Yadav' ,'Umar Gul' ,'V Pratap Singh',
 'V Sehwag' ,'V Shankar', 'VR Aaron' ,'VRV Singh', 'VS Malik' ,'VS Yeligati',
 'VY Mahesh' ,'WD Parnell' ,'WPUJC Vaas' ,'Washington Sundar' ,'Y Nagar'
 'Y Prithvi Raj' ,'Y Venugopal Rao' ,'YA Abdulla' ,'YK Pathan' ,'YS Chahal',
 'Z Khan']
        bowler_add=999
        for i in range(len(batsman_list)):
            if (bowler_list[i] == bowler):
                bowler_add= i
        innings = int(request.form['Innings'])


        if(venue_add==999 or innings>2 or batsman_add==999 or bowler_add==999):
            return render_template('result.html', lower_limit=45, upper_limit=50)
        else:
            temp_array =[venue_add,innings,bat_team,bowl_team,batsman_add,bowler_add]
            data = np.array([temp_array])
            my_prediction = int(regressor.predict(data)[0])
            return render_template('result.html', lower_limit=my_prediction - 3, upper_limit=my_prediction + 3)


if __name__ == '__main__':
    app.run(debug=True)