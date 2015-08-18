class SearchController < ApplicationController
	def search
    @all_recipes = Recipe.all

    @recipes = []
    search_terms = params[:search].downcase.split
    
    @all_recipes.each do |recipe|
      has_term = false
      title = recipe.title.downcase 
      search_terms.each do |term|
        has_term = true if title.include?(term)
      end

      @recipes << recipe if has_term
    end

    render "search_results"
	end
end
