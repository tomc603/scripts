#!/bin/bash

UNAME=$1
if [ "$UNAME" = "" ]; then
	echo "You MUST enter a username"
else
	USERINFO=`ssh nas-01-mht.dyndns.com "getent passwd $UNAME"`
	UNAME=`echo "$USERINFO" | awk -F ":" '{ print $1 }'`
	USRID=`echo "$USERINFO" | awk -F ":" '{ print $3 }'`
	GRPID=`echo "$USERINFO" | awk -F ":" '{ print $4 }'`
	FULLNAME=`echo "$USERINFO" | awk -F ":" '{ print $5 }'`
	HOMEDIR=`echo "$USERINFO" | awk -F ":" '{ print $6 }'`
	USRSHELL=`echo "$USERINFO" | awk -F ":" '{ print $7 }'`

	echo "Username  : $UNAME"	
	echo "User ID   : $USRID"
	echo "Group ID  : $GRPID"
	echo "Full Name : $FULLNAME"
	echo "Home Dir  : $HOMEDIR"
	echo "Shell     : $USRSHELL"
fi
