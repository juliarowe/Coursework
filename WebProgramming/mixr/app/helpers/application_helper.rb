module ApplicationHelper

  # based of Michael Hartl's Rails Tutorial (www.railstutorial.org)
  def full_title(page_title = '')
    base_title = "Mixr"
    if page_title.empty?
      base_title
    else
      "#{page_title} | #{base_title}"
    end
  end

end
