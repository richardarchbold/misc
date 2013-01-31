#!/usr/bin/python

import sys
sys.path.append('/home/richard/workspace/eamm')

import eamm.backend.database
from datetime import datetime, timedelta
from optparse import OptionParser

def main():

    parser = OptionParser()
    
    # meeting-status filter
    parser.add_option("--meeting-status", dest="meeting_status",
                  help="""Meetings are initially created in status SCHEDULED. When this script
                  is run, it will only consider candidate meetings with status SCHEDULED. You 
                  can use this flag to override this to include TEST meetings.
                  """, default="TEST")

    parser.add_option("--time-frame", dest="time_frame",
                  help="""ALL or DUE (default is DUE). When this script runs, it normally only
                  sends surveys for meetings that are scheduled and are 30 mins or more
                  passed their end-time. By setting ALL, this time restriction is removed.
                  """, default="DUE")  

    parser.add_option("--update-status", dest="update_status",
                  help="""YES or NO (default is NO). When this script runs, it normally  does
                  NOT update the meeting_status to FINISHED, so if you run the script again, it
                  will act on all the same meetings as it did on it's previous run. By setting
                  this option to YES, the script will update the status of each meeting to 
                  FINISHED, so they will not be included in future send_survey runs.
                  """, default="NO") 
    
    (options, sys.argv) = parser.parse_args()
    
    if options.time_frame == "ALL":
        sql = """
        select m.idMeeting, m.idInvite, m.meeting_status, i.title, e.invitee_email_addr
        from EAMM.Meeting as m INNER JOIN EAMM.Invite as i INNER JOIN EAMM.Invitee as e
        ON (m.idInvite = i.idInvite and m.idInvite = e.idInvite)
        where m.meeting_status=%s
        """
        sql_args = [options.meeting_status]
    elif options.time_frame == "DUE":
        buffer_mins = 15
        now = datetime.now()
        new = now - timedelta(minutes=buffer_mins)
        newdb = new.strftime("%Y-%m-%d %H:%M:%S")
    
        sql = """
        select m.idMeeting, m.idInvite, m.meeting_status, i.title, e.invitee_email_addr
        from EAMM.Meeting as m INNER JOIN EAMM.Invite as i INNER JOIN EAMM.Invitee as e
        ON (m.idInvite = i.idInvite and m.idInvite = e.idInvite)
        where m.meeting_status=%s and m.end_time<=%s 
        """
        sql_args = [options.meeting_status, newdb]
        
    db_conn = eamm.backend.database.MyDatabase()
    my_query_results = db_conn.select2(sql, sql_args)
    
    for row in my_query_results:
        #
        # Row
        # idMeeting, idInvite, meeting_status, title, invitee_email_addr
        # Desired
        # id_invite:id_meeting:meeting_title:status:invitee_email_addr:<link>
        
        url = "http://127.0.0.1/eamm/complete_survey.py?var1=%s&var2=%s" % (row[0], row[4])
        line = "%s:%s:%s:%s:%s:%s" % (row[1], row[0], row[3], row[2], row[4], url)
        print line

if __name__ == '__main__':
    main()