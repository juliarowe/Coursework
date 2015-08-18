class ModificationsController < ApplicationController
  def new
    @modification = Modification.new
    redirect_to :back
  end

  def create
    if params[:original_id] and params[:suggestion] and !params[:suggestion].blank?
      id = BSON::ObjectId.from_string(params[:original_id])
      original = RecipeIngredient.where(_id: id).first 
      original = Step.where(_id: id).first if !original
      if original
        @modification = Modification.create(suggestion: params[:suggestion], 
                                   original: original)
        @modification.original.recipe.email_subscribers
      end
    end
    redirect_to :back
  end


  private
    def modification_params 
      params.require(:modification).permit(:suggestion, :value)
    end
end
