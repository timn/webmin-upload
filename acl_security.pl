
do '../web-lib.pl';

# acl_security_form(&options)
# Output HTML for editing security options for the apache module
sub acl_security_form
{

print "<TR><TD COLSPAN=4><B>Use user specific options or the options configured in the module config? </B></TD></TR>";

print "<TR><TD><INPUT TYPE=radio NAME=\"glob_conf\" VALUE=\"1\"", ($_[0]->{'glob_conf'}) ? " CHECKED" : "", "> Use global configuration</TD>\n";
print "<TD><INPUT TYPE=radio NAME=\"glob_conf\" VALUE=\"0\"", (!$_[0]->{'glob_conf'}) ? " CHECKED" : "", "> Use user specific configuration</TD>\n";

print "<TR><TD COLSPAN=4><BR><B>User specific options (only useful if you have enabled them above!)</B></TD></TR>";
print "<TR><TD>User's standard dir:</TD> <TD><INPUT TYPE=text NAME=\"user_dir\" VALUE=\"$_[0]->{'user_dir'}\"></TD></TR>";
print "<TR><TD>User is only allowed to upload to standard dir?</TD>";
print "<TR><TD><INPUT TYPE=radio NAME=\"user_only_stand\" VALUE=\"1\"", ($_[0]->{'user_only_stand'}) ? " CHECKED" : "", "> Yes";
print " <INPUT TYPE=radio NAME=\"user_only_stand\" VALUE=\"0\"", (!$_[0]->{'user_only_stand'}) ? " CHECKED" : "", ">No</TD>\n";
print "<TR><TD>Unix-user for file:</TD> <TD><INPUT TYPE=text NAME=\"uuser\" VALUE=\"$_[0]->{'uuser'}\"> ", &user_chooser_button("uuser", 0, 0), "</TD></TR>";
print "<TR><TD>Unix-group for file:</TD> <TD><INPUT TYPE=text NAME=\"group\" VALUE=\"$_[0]->{'group'}\"> ", &group_chooser_button("group", 0, 0), "</TD></TR>";
print "<TR><TD>Maximum length of file for User:</TD> <TD><INPUT TYPE=text NAME=\"maxlength\" VALUE=\"$_[0]->{'maxlength'}\"></TD></TR>";
print "<TR><TD>MIME-type to accept:</TD> <TD><INPUT TYPE=text NAME=\"acceptmime\" VALUE=\"$_[0]->{'acceptmime'}\"></TD></TR>";

}

# acl_security_save(&options)
# Parse the form for security options for the apache module
sub acl_security_save
{

 $_[0]->{'glob_conf'} = $in{'glob_conf'};
 $_[0]->{'user_dir'} = $in{'user_dir'};
 $_[0]->{'uuser'} = $in{'uuser'};
 $_[0]->{'group'} = $in{'group'};
 $_[0]->{'user_only_stand'} = $in{'user_only_stand'};
 $_[0]->{'maxlength'} = $in{'maxlength'};
 $_[0]->{'acceptmime'} = $in{'acceptmime'};

}

### END.