class Subscriber
  include Mongoid::Document
  field :email, type: String

  belongs_to :recipe

end
