#!/usr/bin/perl


#binmode(STDOUT, ":utf8");

open(DATA,"<rmp.txt") or die "Can't open data";
@lines = <DATA>;
close(DATA);


open(DATA2, ">rmpFixed.txt");


select(DATA2);
$~ = MESSAGE;


%dates;
@date;
$i = 1;
print "[";
foreach $string (@lines) {
	@split = split('        ', $string);
	foreach $string2 (@split){
		if(index($string2, "name") != -1 || index($string2, "rating") != -1){
			@split2 = split(">", $string2);
			if(index(@split2[1], ".") != -1){
				@split3 = split("<", @split2[1]);
				print '"rating":' .  @split3[0] . ",";
			} else {
				@split2[1] =~ s/\s+$//;
				print '"name":"' . @split2[1] . '" },';
			}
			print "\n"
    }
    if(index($string2, "ShowRatings") != -1){
        @split2 = split("\"", $string2);
        print '{ "url":"' .  @split2[1] . '",';
        print "\n"
    }
	}
}
print "]";
=for comment
	$num = @split;
	if ($num >1 && length(@split[1]) > 4) {
		if (index(@split[1], ",") != -1) {
			if (exists($dates{@split[1]})) {

			} else {
			    #print @split[1];
				$dates{@split[1]} = 1;
				push(@date, @split[1]);
				$date = @split[1];
				write TITLE;
			}
		} else {
			if(exists($dates{substr(@split[1],0,-2) . ", 2014\n"})) {

			} else {
				$dates{substr(@split[1],0,-2) . ", 2014\n"} = 1;
				push(@date, substr(@split[1],0,-2) . ", 2014\n");
				$date = substr(@split[1],0,-2) . ", 2014\n";
				write TITLE;
			}
		}
	}
	if (index($string, "/") != -1 && index($string, ",") != -1 && index($string, ":") != -1 && (index($string, "am") != -1 || index($string, "pm") != -1) && (index($string, "0") != -1 || index($string, "1") != -1 ||index($string, "2") != -1 || index($string, "3") != -1||index($string, "4") != -1 || index($string, "5") != -1||index($string, "6") != -1 || index($string, "7") != -1||index($string, "8") != -1 || index($string, "9") != -1)) {
		$string =~ s/^\s+//;
		#print " $string";
		$time = $string;
		$name = @lines[$i];
		$k = 2;
		$message = @lines[$i+1];
		$string = @lines[$i+$k];
		if ($message eq @lines[5] || index($message, '`') != -1) {
			$message = "**********emote/sticker***********";
		}
		write;

		while ((index($string, "`") != -1 || (index($string, "/") != -1 && index($string, ",") != -1 && index($string, ":") != -1) && (index($string, "am") != -1 || index($string, "pm") != -1) && (index($string, "0") != -1 || index($string, "1") != -1 ||index($string, "2") != -1 || index($string, "3") != -1||index($string, "4") != -1 || index($string, "5") != -1||index($string, "6") != -1 || index($string, "7") != -1||index($string, "8") != -1 || index($string, "9") != -1)) == 0 ){
			$message = @lines[$i+$k];
			$k++;
			$string = @lines[$i+$k];
			$length = @lines;
			if ($i+$k > @lines) {
				$numDays = @date;
				print $numDays;
				exit;

			}
			if ($message eq @lines[5] || index($message, '`') != -1) {
				$message = "**********emote/sticker***********";
			}
			write;

		}





	}

	$i+= 1;
}
=cut
close( DATA2 );
