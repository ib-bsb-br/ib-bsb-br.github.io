Jekyll::Hooks.register :site, :post_write do |site|
    `npx -y pagefind --site ${{ github.workspace }}/_site --output-path ${{ github.workspace }}/_site/pagefind`
end
