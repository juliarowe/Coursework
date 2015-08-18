class WelcomeController < ApplicationController
  def index
  	@recipes = Recipe.all.sort{|x, y| y.rating <=> x.rating}
  end
end
