use strict;
use warnings;
package Course;

sub new {
	my $class = shift;
	my $self = {
		_course_code	=>	"",
		_title			=>	"",
		_description	=>	"",
		_prerequisite	=>	"",
		_exclusion		=>	"",
		_distribution_requirement_status	=>	"",
		_breadth_requirement	=>	"",
		_recommended_preparation	=>	"",
		_corequisite	=>	""
	};
	bless $self, $class;
	return $self;
}

sub course_code {
    my ( $self, $course_code ) = @_;
    $self->{ _course_code } = $course_code if defined $course_code;
    return $self->{ _course_code };
}

sub title {
    my ( $self, $title ) = @_;
    $self->{ _title } = $title if defined $title;
    return $self->{ _title };
}

sub description {
    my ( $self, $description ) = @_;
    $self->{ _description } = $description if defined $description;
    return $self->{ _description };
}

sub prerequisite {
    my ( $self, $prerequisite ) = @_;
    $self->{ _prerequisite } = $prerequisite if defined $prerequisite;
    return $self->{ _prerequisite };
}

sub exclusion {
    my ( $self, $exclusion ) = @_;
    $self->{ _exclusion } = $exclusion if defined $exclusion;
    return $self->{ _exclusion };
}

sub distribution_requirement_status {
    my ( $self, $distribution_requirement_status ) = @_;
    $self->{ _distribution_requirement_status } = $distribution_requirement_status if defined $distribution_requirement_status;
    return $self->{ _distribution_requirement_status };
}

sub breadth_requirement {
    my ( $self, $breadth_requirement ) = @_;
    $self->{ _breadth_requirement } = $breadth_requirement if defined $breadth_requirement;
    return $self->{ _breadth_requirement };
}

sub recommended_preparation {
    my ( $self, $recommended_preparation ) = @_;
    $self->{ _recommended_preparation } = $recommended_preparation if defined $recommended_preparation;
    return $self->{ _recommended_preparation };
}

sub corequisite {
    my ( $self, $corequisite ) = @_;
    $self->{ _corequisite } = $corequisite if defined $corequisite;
    return $self->{ _corequisite };
}

sub print {
	my $self = shift;
	print ":" x 80 . "\n\n";
	print "Course Code :\n" . $self->course_code . "\n\n";
	print "Title :\n" . $self->title . "\n\n";
	print "Description:\n" . $self->description . "\n\n";
	print "Prerequisite:\n" . $self->prerequisite . "\n\n";
	print "Exclusion :\n" . $self->exclusion . "\n\n";
	print "Distribution Requirement Status :\n" . $self->distribution_requirement_status . "\n\n";
	print "Breadth Requirement :\n" . $self->breadth_requirement . "\n\n";
	print "Recommended Preparation :\n" . $self->recommended_preparation . "\n\n";
	print "Corequisite :\n" . $self->corequisite . "\n\n";
	print ":" x 80 . "\n";
}

1;