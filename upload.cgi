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
#    Created : 12.02.2003
#

# 12.02.2003 - Created upload.cgi, spin off from index.cgi

#############################################################################

do '../web-lib.pl';
$|=1;
&init_config("upload");

&ReadParseMime();

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

if ($upload_dir !~ /\/$/) {
 $upload_dir .= "/";
}

$upload_success=0;


# Get the file
$upload_success = &handle_upload();

# Spit output
&header("File Upload", "images/upload.gif", undef, undef, undef, undef,
        "<a href=\"about.cgi\">About</a>");

if ($upload_success) {

($dev,$ino,$mode,$nlink,$uid,$gid,$rdev,$size, $atime,$mtime,$ctime,$blksize,$blocks) = stat("$upload_dir$filename");

# Received file sucessfully, not indentation due to <<EOM stuff
print <<EOM;
<br/><br/><i>File successfully uploaded</i><br/><hr size=\"4\" noshade>
<table border=\"0\">
<tr><td>Remote File Name:</td><td>$in{'file_filename'}</td></tr>
<tr><td>Server File Name:</td><td>$filename</td></tr>
<tr><td>Location:</td><td>$upload_dir</td></tr>
<tr><td>File Size:</td><td>$size Bytes</td></tr>
<tr><td>Owner:</td><td>$user.$group ($uid.$gid)</td></tr>
<tr><td>Local Time:</td><td>$ctime</td></tr>

</table>
<hr size=\"4\" noshade>
<br/>
EOM
} else {
  # Typical should never happen since we error() out everything in handle_upload
  print "File upload failed. Ask your local daemon why it failed.\n";
}

&footer("", "module index");



#### SUBS

sub handle_upload {

    if( !$in{'file_filename'} ) {
       &error("Could not extract file name. Forgot to upload file?");
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

    return 1;
} # end of handle_upload 

