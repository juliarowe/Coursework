class VotesController < ApplicationController
  def new
    @vote = Vote.new
  end

  def create
    begin 
      to_be_rated = Modification.find(params[:id])
    rescue Mongoid::Errors::DocumentNotFound
      to_be_rated = Recipe.find(params[:id])
    end
    @vote = Vote.create(rateable: to_be_rated, value: params[:value])
    redirect_to :back, rating: @vote.rateable.rating
  end

  private
    def vote_params
      params.require(:vote).permit(:value)
    end
end
