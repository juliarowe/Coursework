class Recipe 
  include Mongoid::Document
  include Mongoid::Paperclip
  field :title, type: String

  has_many :recipe_ingredients, dependent: :delete
  has_many :steps, dependent: :delete
  has_many :votes, as: :rateable

  validates :title, presence: true, length: { minimum: 2, maximum: 255 }

  accepts_nested_attributes_for :recipe_ingredients, :steps

  has_mongoid_attached_file :image
  validates_attachment_content_type :image, :content_type => ["image/jpg", "image/jpeg", "image/png", "image/gif"]
  validates_attachment_size :image, :less_than => (0.05).megabytes, 
                          :unless => Proc.new {|m| m[:image].nil?}

  def rating
    if self.votes.count > 0
      vote_sum = self.votes.all.inject(0) { |sum, vote| sum + vote.value }
      vote_sum / votes.count
    else
      0
    end
  end

  private
  
    def recipe_params
      params.require(:recipe).permit(:title)
    end
end
