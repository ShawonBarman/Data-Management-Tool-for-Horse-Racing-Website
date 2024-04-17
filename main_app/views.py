from django.shortcuts import render
import pandas as pd
import datetime
from .models import *
from django.core.paginator import Paginator
from django.db import transaction
import glob

def extract_date_from_filename(filename):
    date_str = filename.split('-')[:3]
    year, month, day = map(int, date_str)
    return datetime.date(year, month, day)

def clean_currency(value):
    value = str(value)
    value = value.replace('$', '').replace(',', '').replace(' ', '')
    return float(value.strip())

def safe_int(value):
    try:
        return int(value) if value != '' else None
    except ValueError:
        return None

def safe_float(value):
    try:
        return float(value) if value != '' else None
    except ValueError:
        return None
    
def import_data_for_all_meetings_file(all_meetings_file, all_meetings_file_date):
    try:
        if all_meetings_file.name.endswith('.csv'):
            df = pd.read_csv(all_meetings_file)
        elif all_meetings_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(all_meetings_file)
        else:
            raise ValueError("Unsupported file format")
        
        df.columns = df.columns.str.replace(' ', '')
        for index, row in df.iterrows():
            for key, value in row.items():
                if value == '-':
                    row[key] = ''
        df['FormMtgDate'] = pd.to_datetime(df['FormMtgDate'], dayfirst=True).dt.strftime('%Y-%m-%d')
        df['foaldate'] = pd.to_datetime(df['foaldate'], dayfirst=True).dt.strftime('%Y-%m-%d')
        df['Date'] = pd.to_datetime(df['Date'], dayfirst=True).dt.strftime('%Y-%m-%d')
        df['FormMtgDate-2'] = pd.to_datetime(df['FormMtgDate-2'], dayfirst=True).dt.strftime('%Y-%m-%d')
        df['FormMtgDate-3'] = pd.to_datetime(df['FormMtgDate-3'], dayfirst=True).dt.strftime('%Y-%m-%d')
        df = df.fillna('')

        with transaction.atomic():
            records = []
            for index, row in df.iterrows():
                formMtgDate = row['FormMtgDate'] if row['FormMtgDate'] != '' else None
                date = row['Date'] if row['Date'] != '' else None
                foaldate = row['foaldate'] if row['foaldate'] != '' else None
                formMtgDate2 = row['FormMtgDate-2'] if row['FormMtgDate-2'] != '' else None
                formMtgDate3 = row['FormMtgDate-3'] if row['FormMtgDate-3'] != '' else None

                record = AllMeetingsData(
                    file_date=all_meetings_file_date,
                    race_number=safe_int(row['RaceNumber']),
                    tab_number=safe_int(row['TabNo']),
                    horse=row['Horse'],
                    weight=safe_float(row['Weight']),
                    claim=safe_float(row['Claim']),
                    jockey=row['Jockey'],
                    trainer=row['Trainer'],
                    raceId=safe_int(row['RaceId']),
                    jockeyId=safe_int(row['JockeyId']),
                    trainerId = safe_int(row['TrainerId']),
                    meeting=row['Meeting'],
                    track_condition=row['Tr-Cond'],
                    barrier=safe_int(row['Barrier']),
                    reliable=row['Reliable'],
                    class_change=row['ClassChange'],
                    hist_run_style=row['HistRunStyle'],
                    pred_stlg_pos=safe_int(row['PredStlgPos']),
                    pf_score=safe_int(row['PFScore0-100']),
                    avg_hist_settling_pos=safe_float(row['AverageHistoricalSettlingPos%']),
                    neural_price=safe_float(row['NeuralPrice']),
                    neural_rank=safe_int(row['NeuralRank']),
                    rsfi=safe_float(row['RSFI']),
                    last_600m_ranking_late_speed=safe_float(row['Last600mRankingLateSpeed']),
                    s_price=safe_float(row['SPrice']),
                    tp20p=safe_float(row['TP20P']),
                    time_ranking_start_to_finish=safe_float(row['TimeRankingStarttoFinish']),
                    wp20p=safe_float(row['WP20P']),
                    weight_class_rank=safe_int(row['WeightClassRank']),
                    wptp20p=safe_float(row['WPTP20P']),
                    time_adjust_weight_class_rank=safe_int(row['TimeAdjust-Weight/ClassRank']),
                    etr_price=safe_float(row['ETRPrice']),
                    early_time_ranking_to_600m_speed=safe_float(row['EarlyTimeRankingto600mSpeed']),
                    horseId=safe_int(row['HorseId']),
                    distance=safe_float(row['Distance']),
                    race_class=row['RaceCl'],
                    grade=row['grade'],
                    horse_age=safe_int(row['horseage']),
                    horse_sex=row['horsesex'],
                    form_last_10=row['FormLast10'],
                    horse_record=row['HorseRecord'],
                    record_distance=row['RecordDist'],
                    record_track=row['RecordTrack'],
                    record_track_distance=row['RecordTrk-Dist'],
                    record_firm=row['RecordFirm'],
                    record_good=row['RecordGood'],
                    record_soft=row['RecordSoft'],
                    record_heavy=row['RecordHeavy'],
                    first_up_record=row['FirstUpRecord'],
                    second_up_record=row['SecondUpRecord'],
                    form_barrier_1=safe_int(row['FormBarrier-1']),
                    form_class_1=row['FormCl-1'],
                    form_distance_1=row['FormDist-1'],
                    form_jockey_1=row['FormJky-1'],
                    form_margin_1=safe_float(row['FormMargin-1']),
                    form_mtg_date_1=formMtgDate,
                    form_other_runners_1=row['FormOtherRunners-1'],
                    form_pos_1=safe_int(row['FormPos-1']),
                    form_price_1=safe_float(row['FormPrice-1']),
                    form_time_1=row['FormTime-1'],
                    form_track_1=row['FormTrack-1'],
                    form_tr_cond_1=row['FormTr-Cond-1'],
                    form_weight_1=safe_float(row['FormWeight-1']),
                    meeting_id=safe_int(row['meetingid']),
                    race_id=safe_int(row['raceid']),
                    horse_id=safe_int(row['horseid']),
                    foal_date=foaldate,
                    sec_time_1=row['SecTime-1'],
                    time=row['Time'],
                    runner_time=safe_float(row['RunnerTime']),
                    race_starts=safe_int(row['RaceStarts']),
                    race_wins=safe_int(row['RaceWins']),
                    dist_starts=safe_int(row['DistStarts']),
                    dist_wins=safe_int(row['DistWins']),
                    track_starts=safe_int(row['TrackStarts']),
                    track_wins=safe_int(row['TrackWins']),
                    tr_dist_starts=safe_int(row['Tr-DistStarts']),
                    tr_dist_wins=safe_int(row['Tr-DistWins']),
                    good_starts=safe_int(row['GoodStarts']),
                    good_wins=safe_int(row['GoodWins']),
                    soft_starts=safe_int(row['SoftStarts']),
                    soft_wins=safe_int(row['SoftWins']),
                    heavy_starts=safe_int(row['HeavyStarts']),
                    heavy_wins=safe_int(row['HeavyWins']),
                    first_up_starts=safe_int(row['1stUpStarts']),
                    first_up_wins=safe_int(row['1stUpWins']),
                    second_up_starts=safe_int(row['2ndUpStarts']),
                    second_up_wins=safe_int(row['2ndUpWins']),
                    first_up_placings=safe_int(row['1stUpPlacings']),
                    second_up_placings=safe_int(row['2ndUpPlacings']),
                    race_placings=safe_int(row['RacePlacings']),
                    dist_placings=safe_int(row['DistPlacings']),
                    track_placings=safe_int(row['TrackPlacings']),
                    tr_dist_placings=safe_int(row['Tr-DistPlacings']),
                    good_placings=safe_int(row['GoodPlacings']),
                    soft_placings=safe_int(row['SoftPlacings']),
                    heavy_placings=safe_int(row['HeavyPlacings']),
                    rfs=row['RFS'],
                    rfs_count=safe_int(row['RFS_Count']),
                    date=date,
                    last_600m=safe_float(row['Last600m']),
                    dist_sr=safe_float(row['DistSR']),
                    win_sr=safe_float(row['WinSR']),
                    track_sr=safe_float(row['TrackSR']),
                    tr_dist_sr=safe_float(row['Tr-DistSR']),
                    good_sr=safe_float(row['GoodSR']),
                    soft_sr=safe_float(row['SoftSR']),
                    heavy_sr=safe_float(row['HeavySR']),
                    first_up_sr=safe_float(row['1stUpSR']),
                    second_up_sr=safe_float(row['2ndUpSR']),
                    dlr_1=safe_int(row['DLR-1']),
                    form_barrier_2=safe_int(row['FormBarrier-2']),
                    form_class_2=row['FormClass-2'],
                    form_distance_2=row['FormDist-2'],
                    form_jockey_2=row['FormJky-2'],
                    form_margin_2=safe_float(row['FormMargin-2']),
                    form_mtg_date_2=formMtgDate2,
                    form_other_runners_2=row['FormOtherRunners-2'],
                    form_pos_2=safe_int(row['FormPos-2']),
                    form_price_2=safe_float(row['FormPrice-2']),
                    form_track_2=row['FormTrack-2'],
                    form_tr_cond_2=row['FormTrCond-2'],
                    form_weight_2=safe_float(row['FormWeight-2']),
                    form_time_2=row['FormTime-2'],
                    sec_time_2=row['SecTime-2'],
                    dlr_2=safe_int(row['DLR-2']),
                    form_barrier_3=safe_int(row['FormBarrier-3']),
                    form_class_3=row['FormClass-3'],
                    form_distance_3=row['FormDist-3'],
                    form_jockey_3=row['FormJky-3'],
                    form_margin_3=safe_float(row['FormMargin-3']),
                    form_mtg_date_3=formMtgDate3,
                    form_other_runners_3=row['FormOtherRunners-3'],
                    form_pos_3=safe_int(row['FormPos-3']),
                    form_price_3=safe_float(row['FormPrice-3']),
                    form_track_3=row['FormTrack-3'],
                    form_tr_cond_3=row['FormTrCond-3'],
                    form_weight_3=safe_float(row['FormWeight-3']),
                    form_time_3=row['FormTime-3'],
                    sec_time_3=row['SecTime-3'],
                    dlr_3=safe_int(row['DLR-3']),
                    seconds=safe_float(row['Seconds']),
                    msecs=safe_float(row['MSecs']),
                    time1=safe_float(row['Time1']),
                    wght_chg=safe_float(row['WghtChg']),
                    dist_chg=safe_float(row['DistChg']),
                    bar_chg=safe_float(row['BarChg']),
                    wght_over_limit=safe_float(row['Wght_Over_Limit']),
                    ave_spd=safe_float(row['AveSpd(Mts/Sec)']),
                    dbr_1_2=safe_int(row['DBR-1/2']),
                    dbr_2_3=safe_int(row['DBR-2/3']),
                    bf_rtd_price=safe_float(row['BF_RtdPrice']),
                    mktrk=safe_int(row['MktRk']),
                    starters=safe_int(row['Starters'])
                )
                records.append(record)
            AllMeetingsData.objects.bulk_create(records)
    except Exception as e:
        print(e)
        return False, e
    return True, ''
    
def import_data_for_form_all_meetings_file(form_all_meetings_file, form_all_meetings_file_date):
    try:
        if form_all_meetings_file.name.endswith('.csv'):
            df = pd.read_csv(form_all_meetings_file)
        elif form_all_meetings_file.name.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(form_all_meetings_file)
        else:
            raise ValueError("Unsupported file format")
        
        df = df.fillna('')
        df.columns = df.columns.str.replace(' ', '')
        df['formmeetingdate'] = pd.to_datetime(df['formmeetingdate'], format='%d/%m/%y').dt.strftime('%Y-%m-%d')
        df['foaldate'] = pd.to_datetime(df['foaldate'], dayfirst=True).dt.strftime('%Y-%m-%d')
        df['horseprizemoney'] = df['horseprizemoney'].apply(clean_currency)
        df['prizemoney'] = df['prizemoney'].apply(clean_currency)
        df['prizemoneywon'] = df['prizemoneywon'].apply(clean_currency)

        with transaction.atomic():
            records = []
            for index, row in df.iterrows():
                formmeetingdate = row['formmeetingdate'] if row['formmeetingdate'] != '' else None
                foaldate = row['foaldate'] if row['foaldate'] != '' else None
                record = FormAllMeetingsData(
                    file_date=form_all_meetings_file_date,
                    meeting_date=row['meetingdate'],
                    track=row['track'],
                    race_number=safe_int(row['racenumber']),
                    start_time=row['starttime'],
                    distance=safe_float(row['distance']),
                    age_restrictions=row['agerestrictions'],
                    class_restrictions=row['classrestrictions'],
                    weight_restrictions=safe_float(row['weightrestrictions']),
                    race_prizemoney=row['raceprizemoney'],
                    sex_restrictions = row['sexrestrictions'],
                    weight_type=row['weighttype'],
                    race_name=row['racename'],
                    jockeys_can_claim=row['jockeyscanclaim'],
                    grade=row['grade'],
                    horse_name=row['horsename'],
                    horse_age=safe_int(row['horseage']),
                    horse_sex=row['horsesex'],
                    horse_sire=row['horsesire'],
                    horse_dam=row['horsedam'],
                    horse_number=safe_int(row['horsenumber']),
                    horse_jockey=row['horsejockey'],
                    horse_barrier=safe_int(row['horsebarrier']),
                    horse_trainer=row['horsetrainer'],
                    horse_weight=safe_float(row['horseweight']),
                    horse_claim=safe_float(row['horseclaim']),
                    horse_last10=row['horselast10'],
                    horse_record=row['horserecord'],
                    horse_record_distance=row['horserecorddistance'],
                    horse_record_track=row['horserecordtrack'],
                    horse_record_track_distance=row['horserecordtrackdistance'],
                    horse_record_firm=row['horserecordfirm'],
                    horse_record_good=row['horserecordgood'],
                    horse_record_soft=row['horserecordsoft'],
                    horse_record_heavy=row['horserecordheavy'],
                    horse_record_jumps=row['horserecordjumps'],
                    horse_record_firs_up=row['horserecordfirstup'],
                    horse_record_second_up=row['horserecordsecondup'],
                    horse_price_money=safe_float(row['horseprizemoney']),
                    form_barrier=safe_int(row['formbarrier']),
                    form_class=row['formclass'],
                    form_distance=safe_float(row['formdistance']),
                    form_jockey=row['formjockey'],
                    form_margin=safe_float(row['formmargin']),
                    form_meeting_date=formmeetingdate,
                    form_name=row['formname'],
                    form_other_runners=row['formotherrunners'],
                    form_position=safe_int(row['formposition']),
                    form_price=safe_float(row['formprice']),
                    form_time=row['formtime'],
                    form_track=row['formtrack'],
                    form_track_condition=row['formtrackcondition'],
                    form_weight=safe_float(row['formweight']),
                    horse_record_synthetic=row['horserecordsynthetic'],
                    meeting_id=safe_int(row['meetingid']),
                    race_id=safe_int(row['raceid']),
                    horse_id=safe_int(row['horseid']),
                    horse_trainer_id=safe_int(row['horsetrainerid']),
                    horse_jockey_id=safe_int(row['horsejockeyid']),
                    form_trainer_id=safe_int(row['formtrainerid']),
                    form_jockey_id=safe_int(row['formjockeyid']),
                    foal_date=foaldate,
                    pricemoney=safe_float(row['prizemoney']),
                    sectional=row['sectional'],
                    pricemoney_won=safe_float(row['prizemoneywon']),
                    country=row['country'],
                )
                records.append(record)
            FormAllMeetingsData.objects.bulk_create(records)
    except Exception as e:
        print(e)
        return False, e
    return True, ''

def import_data_for_meeting_ratings_file(meeting_ratings_file, meeting_ratings_file_date):
    try:
        data = {}
        if meeting_ratings_file.name.endswith('.csv'):
            meeting_ratings_file_data = pd.read_csv(meeting_ratings_file)
            csv_files = glob.glob(meeting_ratings_file)
            for csv_file in csv_files:
                sheet_name = csv_file.split('.')[0]
                data[sheet_name] = pd.read_csv(csv_file)
        elif meeting_ratings_file.name.endswith(('.xls', '.xlsx')):
            meeting_ratings_file_data = pd.ExcelFile(meeting_ratings_file)
            sheet_names = meeting_ratings_file_data.sheet_names
            for sheet_name in sheet_names:
                data[sheet_name] = pd.read_excel(meeting_ratings_file_data, sheet_name)
        else:
            raise ValueError("Unsupported file format")
        with transaction.atomic():
            records = []
            for sheet_name, df in data.items():
                df = df.fillna('')
                df.columns = df.columns.str.replace(' ', '')
                for index, row in df.iterrows():
                    record = MeetingRating(
                        file_date=meeting_ratings_file_date,
                        meeting=row['Meeting'],
                        track_condition=row['Tr-Cond'],
                        time=row['Time'],
                        race_number=safe_int(row['RaceNo']),
                        race_class=row['RaceClass'],
                        class_change=safe_float(row['ClassChange']),
                        distance=safe_float(row['Distance']),
                        distance_change=safe_float(row['DistChg']),
                        form_last_10=row['FormLast10'],
                        tab_no=safe_int(row['TabNo']),
                        horse=row['Horse'],
                        barrier=safe_int(row['Barrier']),
                        barrier_change=safe_float(row['BarChg']),
                        prediction=safe_float(row['Prediction']),
                        rating=safe_float(row['Rating']),
                        jky=safe_float(row['Jky']),
                        trn=safe_float(row['Trn']),
                        rank_class=safe_int(row['Rank_Class']),
                        rank_lsf_pos=safe_float(row['Rank_LSFPos']),
                        rank_lsf_pos_2=safe_float(row['Rank_LSFPos-2']),
                        rank_dist_chg=safe_float(row['Rank_DistChg']),
                        rank_dlr=safe_float(row['Rank_DLR']),
                        rank_mkt_rk=safe_float(row['Rank_MktRk']),
                        rank_rfs=safe_float(row['Rank_RFS']),
                        rank_pfscore=safe_float(row['Rank_PFScore']),
                        rank_stlg_pos=safe_float(row['Rank_StlgPos']),
                        rank_barrier=safe_float(row['Rank_Barrier']),
                        rank_weight=safe_float(row['Rank_Weight']),
                        jockey=row['Jockey'],
                        jockey_a2e=safe_float(row['Jky_A2E']),
                        weight=safe_float(row['Weight']),
                        weight_change=safe_float(row['WghtChg']),
                        price_sp=safe_float(row['priceSP']),
                        hist_run_style=row['HistRunStyle'],
                        pred_stlg_pos=safe_float(row['PredStlgPos']),
                        trainer=row['Trainer'],
                        trainer_a2e=safe_float(row['Trn_A2E']),
                        mkt_rk=safe_float(row['MktRk']),
                        dlr_1=safe_float(row['DLR-1']),
                        form_margin_1=safe_float(row['FormMargin-1']),
                        form_dist_1=safe_float(row['FormDist-1']),
                        runner_time=safe_float(row['RunnerTime']),
                        last_600m=safe_float(row['Last600m']),
                        ave_spd_mts_sec=safe_float(row['AveSpd(Mts/Sec)']),
                        form_jky_1=row['FormJky-1'],
                        form_weight_1=safe_float(row['FormWeight-1']),
                        form_barrier_1=safe_int(row['FormBarrier-1']),
                        form_tr_cond_1=row['FormTr-Cond-1'],
                        form_cl_1=row['FormCl-1'],
                        form_other_runners_1=row['FormOtherRunners-1'],
                        form_margin_2=safe_float(row['FormMargin-2']),
                        form_dist_2=safe_float(row['FormDist-2']),
                        form_time_2=row['FormTime-2'],
                        sec_time_2=row['SecTime-2'],
                        form_jky_2=row['FormJky-2'],
                        form_weight_2=safe_float(row['FormWeight-2']),
                        form_barrier_2=safe_int(row['FormBarrier-2']),
                        form_tr_cond_2=row['FormTrCond-2'],
                        form_class_2=row['FormClass-2'],
                        form_other_runners_2=row['FormOtherRunners-2'],
                        starts=safe_int(row['Starts']),
                        w_sr=safe_float(row['W-SR']),
                        dist_st=safe_float(row['Dist-St']),
                        dist_sr=safe_float(row['DistSR']),
                        tr_st=safe_float(row['Tr-St']),
                        tr_sr=safe_float(row['Tr-SR']),
                        g_st=safe_float(row['G-St']),
                        g_w=safe_float(row['G-W']),
                        g_sr=safe_float(row['G-SR']),
                        s_st=safe_float(row['S-St']),
                        s_w=safe_float(row['S-W']),
                        s_sr=safe_float(row['S-SR']),
                        h_st=safe_float(row['H-St']),
                        h_w=safe_float(row['H-W']),
                        h_sr=safe_float(row['H-SR']),
                        starters=safe_int(row['Starters'])
                    )
                    records.append(record)
            MeetingRating.objects.bulk_create(records)
    except Exception as e:
        print(e)
        return False, e
    return True, ''

# Create your views here.
def home_page_view(request):
    try:
        if request.method == "POST":
            all_meetings_file = None
            form_all_meetings_file = None
            meeting_ratings_file = None
            message = ''
            all_meetings_file_flag = False
            form_all_meetings_file_flag = False
            try:
                all_meetings_file = request.FILES['all_meetings_file']
            except KeyError:
                pass
            try:
                form_all_meetings_file = request.FILES['form_all_meetings_file']
            except KeyError:
                pass
            try:
                meeting_ratings_file = request.FILES['meeting_ratings_file']
            except KeyError:
                pass
            
            if all_meetings_file:
                try:
                    all_meetings_file_date = extract_date_from_filename(all_meetings_file.name)
                except:
                    return render(request, "home_page.html", {"error_msg": "Date format is missing in your file name."})
                success, error = import_data_for_all_meetings_file(all_meetings_file, all_meetings_file_date)
                if success:
                    message = "All Meetings File has been imported sucessfully."
                    all_meetings_file_flag = True
                else:
                    return render(request, "home_page.html", {"error_msg": error})
            if form_all_meetings_file:
                try:
                    form_all_meetings_file_date = extract_date_from_filename(form_all_meetings_file.name)
                except:
                    return render(request, "home_page.html", {"error_msg": "Date format is missing in your file name."})
                success, error = import_data_for_form_all_meetings_file(form_all_meetings_file, form_all_meetings_file_date)
                if success:
                    if message != '':
                        message = "All Meetings File and Form-All Meetings File have been imported sucessfully."
                    else:
                        message = "Form-All Meetings File has been imported sucessfully."
                    form_all_meetings_file_flag = True
                else:
                    return render(request, "home_page.html", {"error_msg": error})
            if meeting_ratings_file:
                try:
                    meeting_ratings_file_date = extract_date_from_filename(meeting_ratings_file.name)
                except:
                    return render(request, "home_page.html", {"error_msg": "Date format is missing in your file name."})
                success, error = import_data_for_meeting_ratings_file(meeting_ratings_file, meeting_ratings_file_date)
                if success:
                    if all_meetings_file_flag and form_all_meetings_file_flag:
                        message = "All Meetings File, Form-All Meetings File and Meeting Ratings File have been imported sucessfully."
                    elif all_meetings_file_flag and not(form_all_meetings_file_flag):
                        message = "All Meetings File and Meeting Ratings File have been imported sucessfully."
                    elif not(all_meetings_file_flag) and form_all_meetings_file_flag:
                        message = "Form-All Meetings File and Meeting Ratings File have been imported sucessfully."
                    else:
                        message = "Meeting Ratings File has been imported sucessfully."
                else:
                    return render(request, "home_page.html", {"error_msg": error})
            return render(request, "home_page.html", {"success_msg": message})
        return render(request, "home_page.html")
    except Exception as e:
        print(e)
        return render(request, "home_page.html", {"error_msg": e})
    
def allMeetingsData_view(request):
    try:
        if request.method == "POST":
            search_date = request.POST.get("search_date")
            search_date = datetime.datetime.strptime(search_date, '%m/%d/%Y').date()
            filtered_data = AllMeetingsData.objects.filter(file_date = search_date)
            current_date = search_date
            if filtered_data:
                paginator = Paginator(filtered_data, 20)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
            else:
                page_obj = None
        else:
            filtered_data = AllMeetingsData.objects.all()
            current_date = None
            if filtered_data:
                paginator = Paginator(filtered_data, 20)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
            else:
                page_obj = None
        context = {
            # 'filtered_data' : filtered_data,
            'current_date' : current_date,
            'page_obj' : page_obj,
        }
        return render(request, 'allMeetingsData_view_page.html', context)
    except Exception as e:
        filtered_data = AllMeetingsData.objects.all()
        current_date = None
        if filtered_data:
            paginator = Paginator(filtered_data, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
            page_obj = None
        context = {
            'current_date' : current_date,
            'page_obj' : page_obj,
            'error_msg': f"Error: {e}",
        }
        return render(request, 'allMeetingsData_view_page.html', context)
    
def fromAllMeetingsData_view(request):
    try:
        if request.method == "POST":
            search_date = request.POST.get("search_date")
            search_date = datetime.datetime.strptime(search_date, '%m/%d/%Y').date()
            filtered_data = FormAllMeetingsData.objects.filter(file_date = search_date)
            current_date = search_date
            if filtered_data:
                paginator = Paginator(filtered_data, 20)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
            else:
                page_obj = None
        else:
            filtered_data = FormAllMeetingsData.objects.all()
            current_date = None
            if filtered_data:
                paginator = Paginator(filtered_data, 20)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
            else:
                page_obj = None
        context = {
            # 'filtered_data' : filtered_data,
            'current_date' : current_date,
            'page_obj' : page_obj,
        }
        return render(request, 'fromAllMeetingsData_view_page.html', context)
    except Exception as e:
        filtered_data = FormAllMeetingsData.objects.all()
        current_date = None
        if filtered_data:
            paginator = Paginator(filtered_data, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
            page_obj = None
        context = {
            'current_date' : current_date,
            'page_obj' : page_obj,
            'error_msg': f"Error: {e}",
        }
        return render(request, 'fromAllMeetingsData_view_page.html', context)
    
def meetingsRatingData_view(request):
    try:
        if request.method == "POST":
            search_date = request.POST.get("search_date")
            search_date = datetime.datetime.strptime(search_date, '%m/%d/%Y').date()
            filtered_data = MeetingRating.objects.filter(file_date = search_date)
            current_date = search_date
            if filtered_data:
                paginator = Paginator(filtered_data, 20)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
            else:
                page_obj = None
        else:
            filtered_data = MeetingRating.objects.all()
            current_date = None
            if filtered_data:
                paginator = Paginator(filtered_data, 20)
                page_number = request.GET.get('page')
                page_obj = paginator.get_page(page_number)
            else:
                page_obj = None
        context = {
            # 'filtered_data' : filtered_data,
            'current_date' : current_date,
            'page_obj' : page_obj,
        }
        return render(request, 'meetingRatingsData_view_page.html', context)
    except Exception as e:
        filtered_data = MeetingRating.objects.all()
        current_date = None
        if filtered_data:
            paginator = Paginator(filtered_data, 20)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
        else:
            page_obj = None
        context = {
            'current_date' : current_date,
            'page_obj' : page_obj,
            'error_msg': f"Error: {e}",
        }
        return render(request, 'meetingRatingsData_view_page.html', context)

