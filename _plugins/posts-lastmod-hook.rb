#!/usr/bin/env ruby
#
# Check for changed posts

require 'open3'

Jekyll::Hooks.register :posts, :post_init do |post|

  stdout, stderr, status = Open3.capture3('git', 'rev-list', '--count', 'HEAD', post.path.to_s)
  unless status.success?
    Jekyll.logger.warn('lastmod-hook:', "git rev-list failed for #{post.path}: #{stderr.strip}")
    next
  end

  commit_num = stdout.strip

  if commit_num.to_i > 1
    lastmod_stdout, lastmod_stderr, lastmod_status = Open3.capture3('git', 'log', '-1', '--pretty=%ad', '--date=iso', post.path.to_s)
    if lastmod_status.success?
      post.data['last_modified_at'] = lastmod_stdout.strip
    else
      Jekyll.logger.warn('lastmod-hook:', "git log failed for #{post.path}: #{lastmod_stderr.strip}")
    end
  end

end
