#!/usr/bin/perl

#    File Upload Webmin Module
#    Copyright (C) 1999 by Tim Niemueller
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    Created : 12.09.1999
#

# Changes:
# 15.10.1999 - Several improvements, uses not ReadParseMime from Webmin
#            - Cleanup work
#            - added GPL header
#            - Added user and group change capability
#            - Fixed bug in acl_security.pl
#            - added default_acl

#############################################################################

do '../web-lib.pl';
$|=1;
&init_config("upload");

#&read_net_input();
&ReadParseMime();

%access=&get_module_acl;

if (!$config{'standard_dir'}) {
 &error("No global stndard directory given. Check <A HREF=../config.cgi?upload>Module Configuration</A>");
}
if (!$config{'user'}) {
 &error("No global unix user given. Check <A HREF=../config.cgi?upload>Module Configuration</A>");
}
if (!$config{'group'}) {
 &error("No global unix group given. Check <A HREF=../config.cgi?upload>Module Configuration</A>");
}
if ($config{'maxlength'} !~ /^\d+$/) {
 &error("No valid Maxlength given. Check <A HREF=../config.cgi?upload>Module Configuration</A>");
}

if ($access{'glob_conf'})
{
 if ($config{'only_stand'}) {
  $upload_dir=$config{'standard_dir'};
 } else {
  $upload_dir=$in{'dir'};
 }
 $user=$config{'user'};
 $group=$config{'group'};
 $maxl=$config{'maxlength'};
 $mime=$config{'acceptmime'};
} else {
 if ($access{'user_only_stand'}) {
  $upload_dir=$access{'user_dir'};
 } else {
  $upload_dir=$in{'dir'};
 }
 if (!$access{'user'}) {
  &error("No unix user given for user $ENV{'REMOTE_USER'}. Check ",
         "<A HREF=../acl/edit_acl.cgi?mod=upload&user=$ENV{'REMOTE_USER'}>Module ACL</A>");
 }
 if (!$config{'group'}) {
  &error("No unix group given for user $ENV{'REMOTE_USER'}. Check ",
         "<A HREF=../acl/edit_acl.cgi?mod=upload&user=$ENV{'REMOTE_USER'}>Module ACL</A>");
 }
 if ($config{'maxlength'} !~ /^\d+$/) {
  &error("No valid maxlength given for user $ENV{'REMOTE_USER'}. Check ",
         "<A HREF=../acl/edit_acl.cgi?mod=upload&user=$ENV{'REMOTE_USER'}>Module ACL</A>");
 }
 $user=$access{'user'};
 $group=$access{'group'};
 $maxl=$access{'maxlength'};
 $mime=$access{'acceptmime'};
}

$gid=getgrnam($group);
$uid=getpwnam($user);

if (substr($upload_dir, length($upload_dir)-1, 1) ne "/") {
 $upload_dir .= "/";
}

#&header("File Upload", "images/upload.gif", "intro", 1, 1, undef,
#        "Written by<BR><A HREF=mailto:tim\@niemueller.de>Tim Niemueller</A><BR><A HREF=http://www.niemueller.de>Home://page</A>");

$upload_success=0;

if($ENV{'REQUEST_METHOD'} eq 'GET') { &PrintScreen }
else { &handle_upload(); &PrintScreen }

##################################################################
# Print Screen

sub PrintScreen {

&header("File Upload", "images/upload.gif", "intro", 1, 1, undef,
        "Written by<BR><A HREF=mailto:tim\@niemueller.de>Tim Niemueller</A><BR><A HREF=http://www.niemueller.de>Home://page</A>");

if ($upload_success) {

print <<EOM;
<BR><BR><I>File successfully uploaded</I><BR><HR SIZE=4 NOSHADE>
<TABLE BORDER=0>
<TR><TD>Remote File Name:</TD><TD>$in{'file_filename'}</TD></TR>
<TR><TD>Server File Name:</TD><TD>$filename</TD></TR>
<TR><TD>Location:</TD><TD>$upload_dir</TD></TR>
<TR><TD>File Size:</TD><TD>$status_list[4] Bytes</TD></TR>
<TR><TD>Owner:</TD><TD>$user.$group ($uid.$gid)</TD></TR>
<TR><TD>Local Time:</TD><TD>$status_list[5] $status_list[6] $status_list[7]</TD></TR>

</TABLE>
<HR SIZE=4 NOSHADE>
<BR>
EOM

}

print <<EOM;
<BR>

<FORM METHOD="POST" ACTION="$progname" ENCTYPE=multipart/form-data>

<TABLE BORDER=1 CELLPADDING=3 CELLSPACING=0 $cb WIDTH=100%>
<TR><TD>

<TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=0 WIDTH=100%>
<TR><TD $tb>

<TABLE BORDER=0 CELLSPACING=3 CELLPADDING=0 $tb WIDTH=100%>
<TR>
<TD><B>File upload</B></TD>
</TR></TABLE>

</TD></TR>
<TR><TD>
<TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=2 WIDTH=100%>

<TR><TD>
<TABLE BORDER=0 $cb CELLPADDING=0 CELLSPACING=2 WIDTH=100%>
<TR>
<TD>Local file:</TD><TD>
EOM

print "<INPUT TYPE=file NAME=\"file\" ", ($maxl) ? "MAXLENGTH=$maxl " : "",
      ($mime) ? "ACCEPT=$mime " : "", "SIZE=20></TD>\n";

if ( ($access{'glob_conf'} && !$config{'only_stand'}) || (!$access{'glob_conf'} && !$access{'user_only_stand'}) ) {
 print "<TD VALIGN=center>Location: <INPUT TYPE=text NAME=\"dir\" SIZE=20 VALUE=\"$in{'dir'}\">";
 print &file_chooser_button("dir", 1);
 print "</TD>";
}

print <<EOM;
<TD ALIGN=right><INPUT TYPE=submit NAME=\"upload\" VALUE=\"  Upload!  \"></TD>
</TR></TABLE>
</TD></TR></TABLE>
</TD></TR></TABLE>
</TD></TR></TABLE>
</TD></TR></TABLE>



</FORM>

EOM

&footer("/", "webmin index");

} # end of sub PrintScreen




sub handle_upload {


    if( !$in{'file_filename'} ) {
       &error("-- $in{'file_filename'} -- The requested object does not exist on this server.",
              " The link you followed is either outdated, inaccurate, or the server has been",
              " instructed not to let you have it. Connection closed by foreign host.");
    }
    if ($access{'glob_conf'}) {
     if ($config{'acceptmime'} && ($in{'file_content_type'} ne $config{'acceptmime'})) {
      &error("The file you want to upload has the MIME-type '$in{'file_content_type'}'. The only",
             " accepted MIME-type is '$config{'acceptmime'}'.");
     }
    } else {
     if ($access{'acceptmime'} && ($in{'file_content_type'} ne $access{'acceptmime'})) {
      &error("The file you want to upload has the MIME-type $in{'file_content_type'}. The only",
             " accepted MIME-type is $access{'acceptmime'}.");
     }
    }


    $filename   = $in{'file_filename'};
    $filename =~ s/.+\\([^\\]+)$|.+\/([^\/]+)$/\1/;

    $write_file = $upload_dir.$filename;

    open(ULFD,">$write_file") ||  &error("The requested object was not uploaded to the server.",
                                         " <br> Reason : $write_file  $!. The server may have decided not",
                                         " let you write to the directory specified. Please contact the",
                                         " webmaster for this problem. Connection closed by foreign host."); 
    print ULFD $in{'file'};
    close(ULFD);

    chown($uid, $gid, $write_file) || &error("Failed to chown file $write_file to $uid.$gid");

    $upload_success=1;

    1;
} # end of handle_upload 

