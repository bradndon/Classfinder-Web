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
close( DATA2 );
