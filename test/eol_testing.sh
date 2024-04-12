files_to_check=("mixed_eols" "lf_eols" "lf_eols.txt" "crlf_eols" "crlf_eols.csv" "mixed_yaml.yaml" "mixed_yml.yml")

for ftc in ${files_to_check[@]}; do
    # echo "Checking $ftc"
    pre-commit try-repo ../eolchecker eol-checker --files $ftc --verbose > /dev/null
    if [ $? -ne 0 ]; then
        echo "EOL check failed for $ftc"
    fi
done

