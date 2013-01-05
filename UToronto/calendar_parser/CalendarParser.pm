use strict;
use warnings;
use Util;
use Course;
package CalendarParser;
use base qw(HTML::Parser);
use constant COURSE_REGEX => qr/[A-Z]{3}[0-9]{3}[A-Z][0-9]/;

sub new {
	my ( $class, $courses ) = @_;
	my $self = $class->SUPER::new;
	$self->{ _courses } = $courses || {};
	$self->{ _temp_course } = undef;
	$self->{ _temp_course_code } = '';
	$self->{ _temp_property } = '';
	bless $self, $class;
	return $self;
}

sub courses {
    my ( $self, $courses ) = @_;
    $self->{ _courses } = $courses if defined $courses;
    return $self->{ _courses };
}

sub add_course {
	my $self = shift;
	my $course = Course->new;
	my $temp_course = $self->{ _temp_course };
	
	$course->course_code( Util->trim( $self->{ _temp_course_code } ) );
	$course->title( Util->trim( $temp_course->{ title } ) );
	$course->description( Util->trim( $temp_course->{ description } ) );
	$course->prerequisite( Util->trim( $temp_course->{ prerequisite } ) );
	$course->exclusion( Util->trim( $temp_course->{ exclusion } ) );
	$course->distribution_requirement_status( Util->trim( $temp_course->{ 'distribution requirement status' } ) );
	$course->breadth_requirement( Util->trim( $temp_course->{ 'breadth requirement' } ) );
	$course->recommended_preparation( Util->trim( $temp_course->{ 'recommended preparation' } ) );
	$course->corequisite( Util->trim( $temp_course->{ corequisite } ) );
	
	$self->{ _courses }->{ $self->{ _temp_course_code } } = $course;
}

sub start {
	my ( $self, $tagname, $attr, $attrseq, $text ) = @_;
	
	# Check if tag is for a new course code
	if ( $tagname eq 'a' and defined $attr->{ name } ) {
		
		# New 'header' found, so we're done with current course
		$self->add_course if $self->{ _temp_course_code };
		
		# If new 'header' is not a course link skip until we find next course
		if ( not $attr->{ name } =~ COURSE_REGEX ) {
			$self->{ _temp_course_code } = '';
			$self->{ _temp_property } = '';
			return;
		
		# Otherwise, we're looking at a course
		} else {
			# Get new course code, and up next is title
			$self->{ _temp_course_code } = $attr->{ name };
			$self->{ _temp_property } = 'title';
			# Initiate the course object
			$self->{ _temp_course } = {};
			$self->{ _temp_course }->{ title } = '';
			$self->{ _temp_course }->{ description } = '';
			$self->{ _temp_course }->{ prerequisite } = '';
			$self->{ _temp_course }->{ exclusion } = '';
			$self->{ _temp_course }->{ 'distribution requirement status' } = '';
			$self->{ _temp_course }->{ 'breadth requirement' } = '';
			$self->{ _temp_course }->{ 'recommended preparation' } = '';
			$self->{ _temp_course }->{ corequisite } = '';
			return;
		}
	
	# Check if we've reached the end of the page
	} elsif ( $tagname eq 'div' and defined $attr->{ id } and $attr-> { id } eq 'footer' ) {
		$self->add_course if $self->{ _temp_course_code };
		$self->{ _temp_course_code } = '';
		$self->{ _temp_property } = '';
		return;
	}
}

sub text {
	my ( $self, $text, $is_cdata ) = @_;
	
	# Replace HTML &nbsp; with space
	$text =~ s/&nbsp;/ /g;
	
	# Parse the text only if we're looking at a course currently
	if ( $self->{ _temp_course_code } ) {
		
		# If it's a property we expected, switch to the new property
		if ( $text =~ qr/(([Dd]istribution [Rr]equirement [Ss]tatus|[Bb]readth [Rr]equirement|[Pp]rerequisite|[Rr]ecommended [Pp]reparation|[Ee]xclusion|[Cc]orequisite)(\s*?):\s*)/ ) {
			my @texts = split( $1, $text );
			# If there's remaining text before property change, append to the existing property before switching
			$self->{ _temp_course }->{ $self->{ _temp_property } } .= $texts[0] if defined $texts[0];
			# Set new property to lowercase of found label
			$self->{ _temp_property } = lc $2;
			# Set the new text
			$text = $texts[1] || '';
		}
		
		# Add to property
		$self->{ _temp_course }->{ $self->{ _temp_property } } .= $text;
	}
}

sub end {
	my ( $self, $tagname, $text ) = @_;
	
	# Parse the text only if we're looking at a course currently
	if ( $self->{ _temp_course_code } ) {
		
		# If property was title and we've reached the end of span or strong, then up next is description
		if ( ( $tagname eq 'span' or $tagname eq 'strong' ) and $self->{ _temp_property } eq 'title' ) {
			
			# If a title does not exist, then we probably need to keep looking; Dangerous code here!
			return if ( not $self->{ _temp_course }->{ title } );
			
			# Remove course code from title
			my $course_code = $self->{ _temp_course_code };
			$self->{ _temp_course }->{ title } =~ s/$course_code\s+//g;
		
			# If title is just the course code it must not the be actual course link so skip it
			if ( Util->trim( $self->{ _temp_course_code } ) eq Util->trim( $self->{ _temp_course }->{ title } ) ) {
				$self->{ _temp_course_code } = '';
				$self->{ _temp_property } = '';
			
			# Otherwise, on to description!
			} else {
				$self->{ _temp_property } = 'description';
			}
		}
	}
}

1;