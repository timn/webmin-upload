#!/usr/bin/perl

#    File Upload Webmin Module
#    Copyright (C) 1999-2003 by Tim Niemueller
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
# 12.02.2003 - Decided to get rid of all those bug mails :-)
#            - Updated header to make it look nice
#            - split up into index.cgi and upload.cgi
#            - wrote about.cgi
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

%access=&get_module_acl();

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

if (! $access{'glob_conf'}) {
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
}


# real output
&header("File Upload", "images/upload.gif", "intro", 1, 1, undef,
        "<a href=\"about.cgi\">About</a>");


print <<EOM;
<br/>

<form method="POST" action="upload.cgi" enctype="multipart/form-data">
<table border="0">
 <tr>
  <td>Local file:</td>
EOM

print "<td><input type=\"file\" name=\"file\" ", ($maxl) ? "maxlength=\"$maxl\" " : "",
      ($mime) ? "accept=\"$mime\" " : "", "size=\"20\"></td></tr>\n";

if ( ($access{'glob_conf'} && !$config{'only_stand'}) || (!$access{'glob_conf'} && !$access{'user_only_stand'}) ) {
 print "<tr><td>Location:</td><td><input type=\"text\" name=\"dir\" size=\"20\" value=\"$in{'dir'}\">";
 print &file_chooser_button("dir", 1), "</td></tr>\n";
}

print <<EOM;
</table>
<br/>
<input type=\"submit\" name=\"upload\" value=\"  Upload!  \">

</form>
<br/><br/>

EOM

&footer("/", "webmin index");

