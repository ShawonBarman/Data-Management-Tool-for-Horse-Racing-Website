from django.shortcuts import render
import pandas as pd
import datetime
from .models import *
from django.core.paginator import Paginator

def extract_date_from_filename(filename):
    date_str = filename.split('-')[:3]
    year, month, day = map(int, date_str)
    return datetime.date(year, month, day)

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

# Create your views here.
def home_page_view(request):
    try:
        if request.method == "POST":
            all_meetings_file = None
            form_all_meetings_file = None
            meeting_ratings_file = None
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
                if all_meetings_file.name.endswith('.csv'):
                    df = pd.read_csv(all_meetings_file)
                    df = df.fillna('')
                elif all_meetings_file.name.endswith(('.xls', '.xlsx')):
                    df = pd.read_excel(all_meetings_file)
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
                try:
                    all_meetings_file_date = extract_date_from_filename(all_meetings_file.name)
                except:
                    return render(request, "home_page.html", {"error_msg": "Date format is missing in your file name."})
                try:
                    for index, row in df.iterrows():
                        formMtgDate = row['FormMtgDate']
                        if formMtgDate=="":
                            formMtgDate = None
                        else:
                            formMtgDate = row['FormMtgDate']
                        date = row['Date']
                        if date=="":
                            date = None
                        else:
                            date = row['Date']
                        foaldate = row['foaldate']
                        if foaldate=="":
                            foaldate = None
                        else:
                            foaldate = row['foaldate']
                        formMtgDate2 = row['FormMtgDate-2']
                        if formMtgDate2=="":
                            formMtgDate2 = None
                        else:
                            formMtgDate2 = row['FormMtgDate-2']
                        formMtgDate3 = row['FormMtgDate-3']
                        if formMtgDate3=="":
                            formMtgDate3 = None
                        else:
                            formMtgDate3 = row['FormMtgDate-3']
                            
                        allMeetingsData = AllMeetingsData(
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
                            date=None if row['Date']=="" else row['Date'],
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
                        allMeetingsData.save()
                except Exception as e:
                    print(e)
                    return render(request, "home_page.html", {"error_msg": e})
            if form_all_meetings_file:
                if form_all_meetings_file.name.endswith('.csv'):
                    df2 = pd.read_csv(form_all_meetings_file)
                elif form_all_meetings_file.name.endswith(('.xls', '.xlsx')):
                    df2 = pd.read_excel(form_all_meetings_file)
                print(form_all_meetings_file.name)
                print(df2)
                try:
                    form_all_meetings_file_date = extract_date_from_filename(form_all_meetings_file.name)
                except:
                    return render(request, "home_page.html", {"error_msg": "Date format is missing in your file name."})
                print(form_all_meetings_file_date)
            if meeting_ratings_file:
                if meeting_ratings_file.name.endswith('.csv'):
                    df3 = pd.read_csv(meeting_ratings_file)
                elif meeting_ratings_file.name.endswith(('.xls', '.xlsx')):
                    df3 = pd.read_excel(meeting_ratings_file)
                print(meeting_ratings_file.name)
                print(df3)
                try:
                    meeting_ratings_file_date = extract_date_from_filename(meeting_ratings_file.name)
                except:
                    return render(request, "home_page.html", {"error_msg": "Date format is missing in your file name."})
                print(meeting_ratings_file_date)
            return render(request, "home_page.html", {"success_msg": "Data imported successfully."})
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