# Configuration for latexmk to handle bibliographies and glossaries
$pdf_mode = 1;  # Use pdflatex

# Run makeglossaries if necessary
add_cus_dep('glo', 'gls', 0, 'makeglossaries');
add_cus_dep('acn', 'acr', 0, 'makeglossaries');

sub makeglossaries {
    # --- Platform-specific PATH setup ---
    # Uncomment ONE block below if makeglossaries cannot find Perl on your system.
    #
    # Windows (Strawberry Perl — default install path):
    #   local $ENV{PATH} = "C:\\Strawberry\\perl\\bin;" . $ENV{PATH};
    #
    # Windows (Strawberry Perl — custom install path, adjust as needed):
    #   local $ENV{PATH} = "C:\\tools\\strawberry\\perl\\bin;" . $ENV{PATH};
    #
    # macOS (Homebrew Perl):
    #   local $ENV{PATH} = "/opt/homebrew/bin:" . $ENV{PATH};
    #
    # Linux (system Perl is usually on PATH already; if not, specify it):
    #   local $ENV{PATH} = "/usr/bin:" . $ENV{PATH};

    if ( $silent ) {
        system( "makeglossaries -q \"$_[0]\"" );
    }
    else {
        system( "makeglossaries \"$_[0]\"" );
    };
}

# Always try to run bibtex if citations are found
$bibtex_use = 2;
