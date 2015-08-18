class UserMailer < ApplicationMailer
  default from: "mixr@mixr.com"

  def new_modification(email, recipe_title, recipe_id)
    @recipe_title = recipe_title
    @link = "https://fathomless-eyrie-3707.herokuapp.com/recipes/" + recipe_id
    subject = "A new modification for #{recipe_title} was added to Mixr!"
    mail(to: email, subject: subject)
  end
end
