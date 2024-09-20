# frozen_string_literal: true
require 'jekyll-last-modified-at'
module Jekyll
  class LastModifiedAtStringGenerator < Jekyll::Generator
    def generate(site)
      site.posts.docs.each do |post|
        post.data['last_modified_at_str'] = Jekyll::LastModifiedAt::Determinator.new(site.source, post.path, '%Y-%m-%d %H:%M:%S').to_s
      end
    end
  end
end
