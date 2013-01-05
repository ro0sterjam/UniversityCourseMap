#!/usr/bin/perl
# parse-calendar.pl

use strict;
use warnings;
use LWP::UserAgent;
use HTTP::Request;
use HTTP::Response;
use CalendarParser;
use Storable;
use constant BASE_URL => 'http://www.artsandscience.utoronto.ca/ofr/calendar/';

our %links = (	"Planetary Science" => 'crs_pln.htm',
				"Academic Bridging Program" => 'Academic_Bridging_Program.html',
				"French" => 'crs_fre.htm',
				"Centre for Jewish Studies" => 'crs_cjs.htm',
				"Drama" => 'crs_drm.htm',
				"Astronomy and Astrophysics" => 'crs_ast.htm',
				"University College" => 'crs_uni.htm',
				"Mathematics" => 'crs_mat.htm',
				"Life Sciences" => 'Life_Sciences.html',
				"Ecology and Evolutionary Biology" => 'crs_eeb.htm',
				"Classics" => 'crs_cla.htm',
				"English" => 'crs_eng.htm',
				"Anatomy" => 'crs_ana.htm',
				"Victoria College" => 'crs_vic.htm',
				"Trinity College" => 'crs_trn.htm',
				"New College" => 'crs_new.htm',
				"German" => 'crs_ger.htm',
				"Anthropology" => 'crs_ant.htm',
				"Cell and Systems Biology" => 'crs_csb.htm',
				"Public Health Sciences" => 'crs_phs.htm',
				"Comparative Literature" => 'crs_col.htm',
				"Physiology" => 'crs_psl.htm',
				"Human Biology" => 'crs_hmb.htm',
				"199/299/398/399" => '199299398399.html',
				"Rotman Commerce" => 'crs_rsm.htm',
				"Linguistics" => 'crs_lin.htm',
				"Aboriginal Studies" => 'crs_abs.htm',
				"Latin American Studies" => 'crs_las.htm',
				"South Asian Studies" => 'crs_sas.htm',
				"Biology" => 'crs_bio.htm',
				"St. Michael's College" => 'crs_smc.htm',
				"Nutritional Science" => 'crs_nfs.htm',
				"Hungarian" => 'crs_hun.htm',
				"Archaeology" => 'crs_arh.htm',
				"American Studies" => 'crs_usa.htm',
				"Statistics" => 'crs_sta.htm',
				"Modern Languages and Literatures" => 'crs_mll.htm',
				"Peace, Conflict and Justice" => 'crs_pcs.htm',
				"Woodsworth College" => 'crs_wdw.htm',
				"Political Science" => 'crs_pol.htm',
				"Biochemistry" => 'crs_bch.htm',
				"Chemistry" => 'crs_chm.htm',
				"Geography" => 'crs_ggr.htm',
				"Molecular Genetics and Microbiology" => 'crs_mgy.htm',
				"Pharmaceutical Chemistry" => 'crs_phc.htm',
				"Actuarial Science" => 'crs_act.htm',
				"Forest Conservation" => 'crs_for.htm',
				"Psychology" => 'crs_psy.htm',
				"Music" => 'crs_mus.htm',
				"Laboratory Medicine and Pathobiology" => 'crs_lmp.htm',
				"Portuguese" => 'crs_prt.htm',
				"Architecture" => 'crs_arc.htm',
				"Canadian Institute for Theoretical Astrophysics " => 'crs_cta.htm',
				"Immunology" => 'crs_imm.htm',
				"Geology " => 'crs_glg.htm',
				"Cognitive Science" => 'crs_cog.htm',
				"Estonian" => 'crs_est.htm',
				"History and Philosophy of Science and Technology" => 'crs_hps.htm',
				"Near and Middle Eastern Civilizations" => 'crs_nmc.htm',
				"Slavic Languages and Literatures" => 'crs_sla.htm',
				"Philosophy" => 'crs_phl.htm',
				"Spanish" => 'crs_spa.htm',
				"Religion" => 'crs_rlg.htm',
				"History" => 'crs_his.htm',
				"European Studies" => 'crs_eur.htm',
				"Kinesiology &amp; Physical Education" => 'crs_phe.htm',
				"Computer Science" => 'crs_csc.htm',
				"Economics" => 'crs_eco.htm',
				"Physics" => 'crs_phy.htm',
				"Asian Studies, Contemporary" => 'crs_asi.htm',
				"Finnish" => 'crs_fin.htm',
				"Centre for Environment" => 'crs_env.htm',
				"Public Policy " => 'crs_ppg.htm',
				"Diaspora and Transnational Studies" => 'crs_dts.htm',
				"Innis College" => 'crs_ini.htm',
				"East Asian Studies" => 'crs_eas.htm',
				"Sociology" => 'crs_soc.htm',
				"Art" => 'crs_fah.htm',
				"Women and Gender Studies" => 'crs_wgs.htm',
				"Pharmacology and Toxicology" => 'crs_pcl.htm',
				"Joint Courses" => 'crs_jxx.htm',
				"Asia-Pacific Studies" => 'crs_asi.htm',
				"Materials Science" => 'crs_mse.htm',
				"Italian" => 'crs_ita.htm',
				"Ethics" => 'crs_eth.htm',
);

our %programs;
our %courses = ();

sub content_of {
	my $uri = shift;
	my $ua = LWP::UserAgent->new;
	my $request = HTTP::Request->new( GET => $uri );
	return $ua->request( $request )->content;
}

sub parse_calendar {
	foreach my $program_name ( keys %links ) {
		my $link = BASE_URL . $links{ $program_name };
		my $content = content_of $link;
		my $calendar_parser = CalendarParser->new;
		
		print "Parsing $program_name...\n";
		$calendar_parser->parse( $content );
		my $temp_courses = $calendar_parser->courses;
		
		$programs{ $program_name } = $temp_courses;
		%courses = ( %courses, %$temp_courses);
	}
	print "done...\n\n";
}

sub print_courses {
	my $courses = $_[0] || \%courses;
	foreach my $course ( values %$courses ) {
		$course->print;
	}
}

sub save_courses {
	my ( $filename, $courses ) = @_;
	print "Saving courses... ";
	$courses = $courses || \%courses;
	store( $courses, $filename );
	print "done...\n\n";
}

sub load_courses {
	my $filename = shift;
	print "Loading courses... ";
	my $courses = retrieve($filename);
	print "done...\n\n";
	return $courses;
}

sub main {
	#parse_calendar;
	#save_courses( "courses.object" );
	%courses = %{ load_courses( "courses.object" ) };
	#print_courses;
}

main;

sub temp_code {
	my $creg = '[A-Z]{3}[0-9]{3}[A-Z][0-9]';
	my $creg2 = '([A-Z]{3})?[0-9]{3}[A-Z][0-9]?';
	my $grade = '\((minimum)?(grade)?(of)?[0-9][0-9]%(minimum)?\)';
	my $tba = '[Tt][Bb][Aa]';
	my $sep = '([;,\/\(\)+]|or|and){0,3}';
	my $none = '[Nn]one\.?';
	my $fce = "([Mm]inimum)?[0-9]+(\.[0-9])?[Ff][Cc][Ee]'?`?s?([Ii]ncluding)?";
	my $csc = 'CGPA3.0\/[Ee]nrolmentinaCSC[Ss]ubjectPOSt\.?';
	my $year = '(4th|3rd|2nd|1st)[Yy]ear[Ss]tatus';
	my $adv = '[Aa]dvanced[Ss]tatus';
	my $perm = '(([Pp]ermission(of|or)(the)?[Ii]nstructor)|([Pp]ermissionof(the)?[Dd]epartment)|(ApprovalofInstructorandProgramDirector)|(WrittenapprovalofProgramDirector)|(ApprovaloftheUndergraduateCoordinatorisrequired))\.?';
	my $prev = "([Pp]reviously$creg2)";
	my $equ = "(or)?(it'?s)?(their)?(an)?equivalent";

	my $good;
	my $neutral;
	my $evil;
	for my $course ( values %courses ) {
		my $prerequisite = $course->prerequisite;
		my $condensed = $prerequisite;
		$condensed =~ s/\s+//g;
		if ( $condensed =~ m/^$sep($creg$sep)+\.?$/ or not $condensed or $condensed =~ m/^$none$/ ) {
			$good++;
		} elsif ( $condensed =~ m/^$sep(($creg2|$perm|$tba|$fce|$csc|$year|$grade|$adv|$prev|$equ)$sep)+\.?$/ ) {
			$neutral++;
		} else {
			$evil++;
			print ":" x 80 . "\n";
			print $prerequisite . "\n";
		}
	}

	print 'Good : ' . $good . "\n";
	print 'Neut : ' . $neutral . "\n";
	print 'Evil : ' . $evil . "\n";
}
