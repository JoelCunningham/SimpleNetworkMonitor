import { BaseFormSection } from '#components/form-sections';
import { ComponentFixture, TestBed } from '@angular/core/testing';

describe('FormSection', () => {
  let component: BaseFormSection;
  let fixture: ComponentFixture<BaseFormSection>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [BaseFormSection],
    }).compileComponents();

    fixture = TestBed.createComponent(BaseFormSection);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
